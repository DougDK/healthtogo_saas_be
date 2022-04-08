import time
from typing import Any

from flask_sqlalchemy import SignallingSession
from sqlalchemy.orm import Query
from sqlalchemy.exc import OperationalError
from psycopg2.errorcodes import LOCK_NOT_AVAILABLE
from psycopg2.errors import lookup


class H2GSession(SignallingSession):
    """
    Extend SignallingSession -- the default scoped session provided by Flask-SQLAlchemy.
    """

    def __init__(self, *args, **kwargs):
        """
        Locking objects (e.g. using session.query().with_for_update()) can be tricky. Keeping track of whether rows are
        locked in the DB, and when they are unlocked, isn't so straightforward. These extensions attempt to make the session
        API for locking rows more explicit/natural/predictable.

        If you acquire an update lock and then release it (e.g. through the appropriate commit(), rollback(), or close())
        but still have a handle to the objects, you should acquire the lock again if you are going to further update,
        or else you may have created a race condition.

        pending_txns_that_locked_objects + committed_txns_that_locked_objects == "txns that have active row locks in the db"
        """
        self.pending_txns_that_locked_objects = []  # use as stack; allows this session to lock with more than one query
        self.committed_txns_that_locked_objects = []
        super().__init__(*args, **kwargs)

    def commit(self):
        """
        Raises ConcurrencyError if the current txn is one that locked objects. Meant to enforce being explicit and
        aware of locks. Also clears self.committed_txns_that_locked_objects if this is the root txn, since those txns will
        now be actually committed to the db and related locks released.
        Otherwise, same as SignallingSession.commit().
        """
        if self.pending_txns_that_locked_objects and self.pending_txns_that_locked_objects[-1] is self.transaction:
            raise ConcurrencyError('current txn locked objects, use commit_locked to be explicit')
        if not self.transaction.nested:
            self.committed_txns_that_locked_objects.clear()
        super().commit()

    def rollback(self):
        """
        Same as SignallingSession.rollback(), except does some extra internal state management.
        Note, a rollback of a nested transaction that created row locks in the db actually releases those locks in the db
        (in contrast to a commit of a nested transaction: Only a commit of the root transaction releases the lock).
        """
        if self.pending_txns_that_locked_objects and self.pending_txns_that_locked_objects[-1] is self.transaction:
            self.pending_txns_that_locked_objects.pop()
        super().rollback()

    def close(self):
        """
        Same as SignallingSession.close(), except does some extra internal state management.
        """
        self.pending_txns_that_locked_objects.clear()
        self.committed_txns_that_locked_objects.clear()
        super().close()

    def commit_locked(self):
        """
        Commits the current txn if it is one that locked objects; raises ConcurrencyError if not.
        Does *not* release the corresponding lock in the db: commit() only releases locks if it's the root txn for the
        session (and commit() root releases *all* locks in db from previously-committed nested txns).
        Since we created a nested txn when doing the locking, this method won't work if current txn is root.

        Keeps track of the committed, nested txn in self.committed_txns_that_locked_objects so can be referenced if needed.
        """
        if not self.pending_txns_that_locked_objects or self.pending_txns_that_locked_objects[-1] is not self.transaction:
            raise ConcurrencyError('tried to commit txn that locked objects, but the current txn did not lock objects')
        txn = self.pending_txns_that_locked_objects.pop()
        self.commit()
        self.committed_txns_that_locked_objects.append(txn)

    def get_rows_locked_for_update(self, query: Query, of, wait_secs_per_try: float = 0.5, max_tries: int = None,
                                   row_retrieval_func: str = 'all') -> Any:
        """
        What it does: Adds 'FOR UPDATE' and related options to the SQL of the given 'query' arg, then executes that
        query. This puts a lock in the actual database on just the rows targeted by the query, and further on just the columns
        mentioned in the given 'of' arg of those rows.
        The semantics of the 'FOR UPDATE' varies by database. In Postgres, the 'FOR UPDATE' lock serializes queries on the
        locked rows/columns "in other transactions that attempt UPDATE, DELETE, SELECT FOR UPDATE, SELECT FOR NO KEY UPDATE,
        SELECT FOR SHARE or SELECT FOR KEY SHARE". In other words, queries that update/delete/'select for update' the same
        rows/cols are blocked until the lock is released.

        When you would want to use this:
        1) "I need to ensure read+update update is serialized": Let's say you have some column 'counter', and your
            code selects a row, does some stuff, then does row.counter += 1, then commits. SQLAlchemy does not by default
            prevent different transactions from reading committed data then committing updates. Writes -- just the 'update'
            statement part -- are serialized by default, but the whole 'read, do stuff, then update' is *not* serialized.
            So, if you had two different sessions/transactions execute your code concurrently, they might both read '5' for
            counter, do stuff, increment to '6', then commit. But you just lost a tally in the count, because you really wanted
            them serialized so one transaction commits '6' and the next commits '7'. If you use this method in your
            code when querying to get the row, one transaction will acquire the 'FOR UPDATE' lock on the row, and the
            other will block forever (until lock released) or fail after some tries depending on the other args you provided.
            So in the example, if the first transaction gets the lock first, it will read '5' but the other transaction will
            fail to acquire the lock and block/retry. The first will do its thing, commit '6', and release the lock, then the
            other transaction can acquire the lock (if it is still trying), read '6', then correctly increment to '7'.
            This is the 'simplest' example of when you would want to serialize read+update.
        2) "I'm using these rows/cols as a kind of mutex for a broader concept not represented well in the database":
            This is really just an extension of case 1), but applied to data you aren't actually selecting in your query.
            An example of this is our duplicate groups. We do calculations about what materials are in a group,
            what their status is, adding/removing materials, etc, and we need to make sure the data read at
            the beginning of a transaction that does this "business logic" is not changed in the db by other transaction or
            we might have weird results. So, if some transaction wants to change anything about a duplicate group -- calc its
            stats, add/remove a material, merge groups, etc -- we (as programmers) enforce that the code must first acquire
            a 'FOR UPDATE' lock on the relevant row(s) in the material_duplicate_group table. Then the code is free to
            create/modify/delete data in any any table that modifies the meaning of the group(s) (e.g. adding rows in the
            material_duplicate_group_action table).

        How it works:
        Starts a nested transaction with begin_nested() and returns the result of executing the row_retrieval_func
        (e.g. 'all', 'first', etc) of the given query using with_for_update(of=of, nowait=True if max_tries provided).
        Uses a nested transaction because failing to acquire a lock with nowait=True ruins the current transaction, meaning
        any subsequent operation with the session will raise a 'InFailedTransaction' kind of error. So, we begin_nested() before
        each try and rollback() after each failed try. Appends the created nested txn to self.pending_txns_that_locked_objects.
        If max_tries is not provided, nowait=False in the with_for_update, and will potentially block forever.
        Uses populate_existing() on the query before executing to ensure returned data is up-to-date.
        A regular commit() of the created nested transaction will raise an error -- use the explicit commit_locked() instead.
        If raises some error after creating the nested txn, rolls the nested txn back.
        :param query: the query to execute
        :param of: from sqlalchemy docs: "the SQL expression or list of SQL expression elements (typically Column objects or a
            compatible expression) which will render into a FOR UPDATE OF clause;". In other words, the columns of the rows
            that will be locked for update in the DB on successful query execution. Can pass a Model for all columns.
        :param wait_secs_per_try: if max_tries provided, waits this long between executions of the query
            (i.e., attempts at acquiring the rows/lock on those rows)
        :param max_tries: if provided, tries this many times to execute the query. if not, blocks until acquires lock.
        :param row_retrieval_func: the name of the query's func to use when executing query against db:
            supported funcs are {'all', 'first', 'one'}
        :return: result(s) per the query (e.g. 'all' returns a list of objects, 'first' returns an object)
        :raises DBLockFail if max_tries is provided and fails to acquire row locks per the query that many times.
        """
        tries = 0
        if max_tries is None:
            nowait = False
            max_tries = 1
        else:
            nowait = True
        query = query.populate_existing().with_for_update(nowait=nowait, of=of)
        while tries < max_tries:
            self.pending_txns_that_locked_objects.append(self.begin_nested())
            try:
                if row_retrieval_func == 'all':
                    return query.all()
                elif row_retrieval_func == 'first':
                    return query.first()
                elif row_retrieval_func == 'one':
                    return query.one()
                else:
                    raise ValueError(f'row retrieval func "{row_retrieval_func}" not supported')
            except OperationalError as err:
                self.rollback()
                if type(err.orig) == LOCK_NOT_AVAILABLE_ERR_TYPE:
                    tries += 1
                    time.sleep(wait_secs_per_try)
                else:
                    raise
            except Exception:
                self.rollback()
                raise
        raise DBLockFail(f'failed to retrieve rows with update lock in {max_tries} attempts')
