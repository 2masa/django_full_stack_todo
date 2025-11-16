# `dbschema/` (Database Schema)

This directory defines the **EdgeDB** data schema for the project. The schema is written in `.gel` files.

## 📦 Data Models

### `user.gel`
- **`UserType` (abstract):** Base type with `email` and `name`.
- **`RootUser`:** A special user type for the initial admin.
- **`User`:** Standard application user. Extends `Auditable`.
- **`Credential`:** Stores `password` (hashed) and links to a `UserType`.

### `todo.gel`
- **`TodoStatus` (enum):** `Open`, `Completed`, `Pending`, etc.
- **`TodoPriorityStatus` (enum):** `Highest`, `High`, `Medium`, `Low`.
- **`Todo`:** The main todo item.
  - `link user -> User` (required)
  - `property status -> TodoStatus` (required)
  - `property title -> str` (required)
  - `property priority -> TodoPriorityStatus` (required)

### `default.gel`
- **`Auditable` (abstract):** Automatically adds `log_insert` and `log_update` triggers to any type that extends it.
- **`AuditLog`:** A type to record all create/update actions, linking to the `user` who performed them via the `global current_user_id`.
- **`global current_user_id`**: A global variable set by the API to enable auditing.

## 🗄️ Database Migrations

Migrations are managed using the `gel` CLI, which is wrapped by our `devops` tool.

**1. To Create a New Migration:**
After changing a `.gel` file, run this from the `devops/` directory:

```
uv run gel migration create
```