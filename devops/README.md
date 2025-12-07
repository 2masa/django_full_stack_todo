# `devops/` (Developer Tooling & Orchestration)

This directory contains the project's central **developer CLI** and **Docker Compose** configuration. It serves as the main entry point for all local development operations.

The CLI is built with `rich-click` and provides simple commands to manage the entire application stack.

## 🚀 Quick Start

1.  **Install dependencies:**
    ```bash
    uv sync
    ```
2.  **Run the automated "start dev" command:**
    ```bash
    uv run cli service start-dev
    ```
    This single command will:
    * Purge any existing containers and volumes.
    * Generate secure `.env` files.
    * Build and start the full stack (`api`, `ui`, `db`, `redis`).
    * Seed the database with a root admin.
    * **Prompt you** to create your own personal user.

The application will be available at `http://localhost:5000`.

## 🤖 CLI Commands

All commands are executed from this directory using `uv run cli ...`.

### `service` commands
Wrappers for `docker-compose` actions that handle networking and cleanups.

| Command | Description |
| :--- | :--- |
| `service start-dev` | **(Primary)** Full reset: Purges data, creates envs, starts app, and runs setup wizards. |
| `service start` | Starts all services in the background (`docker-compose up -d`). |
| `service stop` | Stops all running services. |
| `service down` | Stops and removes containers (preserves database volumes). |
| `service purge` | **(DESTRUCTIVE)** Stops/removes containers AND permanently deletes data volumes. |

### `env` commands
Manages configuration and secrets.

| Command | Description |
| :--- | :--- |
| `env create` | Generates secure `.env` files in `devops/envs/` (auto-generates keys). |

### `user` commands
Manages database users without needing raw SQL.

| Command | Description |
| :--- | :--- |
| `user create-root`| Seeds the DB with the mandatory `rootadmin@todo.com` user. |
| `user create` | Interactively prompts you to create a new regular `User`. |

## 🌐 Architecture & Networking

The stack uses a custom bridge network (`app_net`) with **Static IPs** to ensure reliable communication between containers.

| Service | Container Name | Internal IP | Port |
| :--- | :--- | :--- | :--- |
| **Backend API** | `todo_api` | `172.20.0.5` | `7000` |
| **Frontend UI** | `todo_ui` | (DHCP) | `5000` |
| **Database** | `todo_db` | (DHCP) | `5656` |