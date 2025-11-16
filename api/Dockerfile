FROM python:3.14.0
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN mkdir -p /opt/api/


WORKDIR /opt/api/

COPY ./app ./app
COPY ./pyproject.toml .
COPY ./uv.lock .

RUN mkdir -p /opt/api/.venv
RUN chmod 777 -R /opt/api/.venv
RUN uv sync 

EXPOSE 7000

cmd uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 7000