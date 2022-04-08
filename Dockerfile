FROM python:3.9.9-slim-bullseye

RUN useradd -ms /bin/bash healthtogo \
    && mkdir -p /app \
    && chown healthtogo /app

USER healthtogo

ENV PATH /home/healthtogo/.local/bin:$PATH

COPY --chown=healthtogo healthtogo/ /app/healthtogo/
COPY --chown=healthtogo conf/ /app/conf/
COPY --chown=healthtogo \
    main.py wsgi.py requirements.txt /app/
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install --user -r requirements.txt

CMD ["gunicorn", "-c", "conf/gunicorn-cfg.py", "wsgi"]