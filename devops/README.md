### Tooling (`devops/`) README Format

This is crucial. It focuses *only* on the CLI commands and what they do.

```markdown
# `devops/` (Developer Tooling & Orchestration)

This directory contains the project's central **developer CLI** and **Docker Compose** file. This is the main entry point for all local development.

The CLI is built with `rich-click` and provides simple commands to manage the entire application stack.

## 🚀 Quick Start

1.  **Install dependencies:**
    ```
    uv sync
    ```
2.  **Run the automated "start dev" command:**
    ```
    uv run cli service start-dev
    ```
This will set up everything and start the application at `http://localhost:5000`.

## 🤖 CLI Commands

All commands are run from this directory (e.g., `uv run cli ...`).

### `service` commands
Wrappers for `docker-compose` actions.

| Command | Description |
| :--- | :--- |
| `service start-dev` | **(Primary)** Purges, creates envs, builds, starts, and seeds DB. |
| `service start` | Starts all services (`docker-compose up -d`). |
| `service stop` | Stops all running services. |
| `service down` | Stops and removes containers (keeps data). |
| `service purge` | **(DESTRUCTIVE)** Stops, removes containers, AND deletes data volumes. |

### `env` commands
Manages environment files.

| Command | Description |
| :--- | :--- |
| `env create` | Generates all `.env` files in `devops/envs/` (including secrets). |

### `user` commands
Manages database users.

| Command | Description |
| :--- | :--- |
| `user create-root`| Seeds the DB with the initial `rootadmin@todo.com` user. |
| `user create` | Interactively prompts you to create a new regular `User`. |