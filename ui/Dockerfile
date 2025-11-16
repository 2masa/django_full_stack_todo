FROM python:3.14.0
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN mkdir -p /opt/ui

WORKDIR /opt/ui

COPY . .
COPY ./pyproject.toml .
COPY ./uv.lock .

RUN mkdir -p /opt/ui/.venv
RUN chmod 777 -R /opt/ui/.venv

EXPOSE 5000

RUN uv sync

CMD uv run app.py