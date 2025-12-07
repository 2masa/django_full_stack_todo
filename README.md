# [To - Do]

<p align="center">
  <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">
  <img src="https://img.shields.io/badge/tech-FastAPI_&_Django-blue" alt="Tech">
  <img src="https://img.shields.io/badge/db-EdgeDB_(Gel)-purple" alt="Database">
</p>

A full-stack Todo application built with a stateless Django frontend and a FastAPI backend, orchestrated via a custom Python CLI.

## 🚀 Quick Start (Local Development)

This project is managed by a central `devops` CLI.

1.  **Navigate to the `devops` directory:**
    ```bash
    cd devops
    ```
2.  **Install CLI dependencies:**
    ```bash
    uv sync
    ```
3.  **Run the automated "start dev" command:**
    ```bash
    uv run cli service start-dev
    ```
This single command will:
- Purge old containers
- Generate all `.env` files and secrets
- Build and start all services (`api`, `ui`, `db`, `redis`)
- Seed the database with a root user
- Prompt you to create a regular user

Your application is now running at **`http://localhost:5000`**.

## 🏛️ Architecture

A high-level overview of the services and how they interact.

```mermaid
graph TD
    User([User's Browser]) -- Views/HTMX --> UI(todo_ui - Django);
    UI -- Stores Session --> Redis(redis);
    UI -- API Calls (JWT) --> API(todo_api - FastAPI);
    API -- Queries --> DB(todo_db - EdgeDB/Gel);

    subgraph "Developer Control"
        Dev(Developer) -- Runs --> CLI(devops/ CLI);
        CLI -- Manages --> Docker(Docker Compose);
        CLI -- Seeds --> DB;
    end
```


## 📁 Project StructureA tree view of the main repositories/folders..

```
├── api/          # Backend FastAPI service
├── ui/           # Frontend Flask/HTMX service
├── db/           # EdgeDB Docker configuration
├── dbschema/     # EdgeDB .gel schema files
├── devops/       # Main CLI, docker-compose.yml, and envs
└── README.md     # This file
```
