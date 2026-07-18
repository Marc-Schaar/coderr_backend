# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /usr/src/app

# libpq5 is the runtime counterpart to the psycopg2-binary wheel, which
# bundles libpq at build time but still links against it at runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# Static assets don't depend on runtime secrets or the database, so they're
# collected once at build time instead of on every container start.
RUN python manage.py collectstatic --noinput

RUN addgroup --system app \
    && adduser --system --ingroup app app \
    && mkdir -p /usr/src/app/media \
    && chmod +x entrypoint.sh \
    && chown -R app:app /usr/src/app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request as u; assert u.urlopen('http://127.0.0.1:8000/admin/login/', timeout=3).status == 200"

ENTRYPOINT ["./entrypoint.sh"]
