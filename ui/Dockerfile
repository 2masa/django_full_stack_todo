FROM python:3.14.0
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN mkdir -p /opt/ui
WORKDIR /opt/ui

COPY . .
# Ensure we have the new dependencies
RUN uv sync

EXPOSE 5000

# Run gunicorn pointing to the new config.wsgi
CMD ["uv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:5000"]