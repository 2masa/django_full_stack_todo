FROM python:3.14.0
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN mkdir -p /opt/ui
WORKDIR /opt/ui

COPY . .
RUN uv sync

RUN FLASK_SECURITY_KEY="build-key" uv run python manage.py collectstatic --noinput

EXPOSE 5000

# Bind to 5000 to match docker-compose
CMD ["uv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:5000"]