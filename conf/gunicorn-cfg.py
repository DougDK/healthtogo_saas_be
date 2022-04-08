import multiprocessing
import os

from healthtogo.core.version import app_version


def on_starting(server):
    server.log.info("Starting web server for Calendar build: %s", app_version())


def on_exit(server):
    server.log.info("GUNICORN EXITING")

import gunicorn

# suppress `server: gunicorn/whateve` header _for security_ - VER-1883
gunicorn.SERVER_SOFTWARE = 'undisclosed-Rei3v'

bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:5000")

# using 'sync' -- e.g. 1:1 process per request -- to be safe
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')

# only meaningful if we use worker_class 'gthread'
threads = int(os.environ.get('GUNICORN_THREADS', 1))


timeout = 90
# grab GUNICORN_CPU_RATIO*num_cpus + 1 by default
# can set to a specific count explicitly with GUNICORN_WORKERS, or
# tune with GUNICORN_CPU_RATIO (a float) in the env.
# finally, you can set a floor on the number of workers with GUNICORN_MIN_WORKERS
workers = max(int(os.environ.get('GUNICORN_MIN_WORKERS', 2)),
              int(os.environ.get("GUNICORN_WORKERS",
                                multiprocessing.cpu_count() *
                                float(os.environ.get('GUNICORN_CPU_RATIO', 2)) + 1)))
