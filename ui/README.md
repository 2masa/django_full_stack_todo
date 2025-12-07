# `ui/` (Frontend Service)

This directory contains the `todo_ui` service, a server-side web application now built with **Django**. It renders the user interface using **Django Templates (DTL)** and **HTMX** for dynamic, single-page-application-like interactions.

## 🛠️ Tech Stack

- **Django**: High-level Python web framework (replaces Flask).
- **WhiteNoise**: Efficient static file serving for production.
- **Gunicorn**: Production-grade WSGI HTTP server.
- **HTMX**: Dynamic UI updates without full page reloads.
- **Django-Redis**: Server-side session storage backed by Redis.
- **Requests**: HTTP library for communicating with the `todo_api`.

## ✨ Key Features

- **Stateless Architecture**: Django is configured to run without a persistent SQL database (using in-memory SQLite only for system checks). Data persistence is handled entirely by the `api` service.
- **Secure Sessions**: User JWTs are stored securely in a server-side **Redis** session, not exposed to the client.
- **API Proxy Layer**: A dedicated `APIClient` service layer handles token injection and communication with the backend.
- **Dynamic UI**: Uses HTMX for:
  - `hx-post` / `hx-delete` for asynchronous form submissions.
  - `hx-target` for partial page updates (swapping tables/modals).
  - `hx-headers` for passing CSRF tokens securely.

## 📂 Project Structure

The project follows a standard Django layout:

- **`config/`**: Project-level configuration (`settings.py`, `urls.py`, `wsgi.py`).
- **`web/`**: The main Django application containing:
  - `views.py`: UI logic and HTMX partial rendering.
  - `services.py`: The HTTP client interacting with the backend API.
  - `templates/`: HTML templates (converted from Jinja2).
  - `templatetags/`: Custom inclusion tags (replacing Jinja macros).
- **`static/`**: CSS, JavaScript, and asset files.
- **`manage.py`**: Django's command-line utility.

## 🔑 Environment Variables

This service is configured via `devops/envs/ui.env`.
*> Note: Variable names currently retain `FLASK_` prefixes to ensure compatibility with the existing DevOps CLI generator.*

| Variable | Django Setting | Description |
| :--- | :--- | :--- |
| `FLASK_SECURITY_KEY` | `SECRET_KEY` | **[SECRET]** Used for cryptographic signing. |
| `FLASK_DEBUG` | `DEBUG` | Toggle debug mode (`true`/`false`). |
| `FASTAPI_BASE_URL` | `FASTAPI_BASE_URL` | Internal URL of the backend API (e.g., `http://todo_api:7000`). |
| `REDIS_HOST` | `CACHES['default']` | Redis service host (e.g., `redis` or IP). |
| `REDIS_PORT` | `CACHES['default']` | Redis service port (e.g., `6379`). |
