from bcrypt import gensalt, hashpw
import rich_click as click
from rich.console import Console
from rich.prompt import Prompt
from app.db import get_sync_client  # This is now a context manager
from edgedb.errors import ConstraintViolationError

console = Console()


@click.group(name="user")
def user() -> None:
    """User management commands."""
    pass


@user.command(name="create-root")
def create_root_user() -> None:
    """
    Creates the first-time root user.
    The email and name are taken from the schema defaults.
    """
    console.print("[bold cyan]Creating Root User...[/bold cyan]")
    
    try:
        with get_sync_client() as client:
            # Check if root user already exists
            root_email = "rootadmin@todo.com" # From user.gel schema
            existing = client.query_single(
                """
                SELECT exists(
                    WITH module user
                    SELECT UserType FILTER .email = <str>$email
                )
                """,
                email=root_email,
            )

            if existing:
                console.print(f"[bold yellow]Root user ({root_email}) already exists. Skipping.[/bold yellow]")
                return

            # Insert RootUser and Credential in one query
            query = """
            WITH 
                module user,
                new_root_user := (
                    INSERT RootUser
                )
            SELECT new_root_user {
                id,
                email,
                name
            }
            """
            new_user = client.query_single(query)
            console.print(f"[bold green]Success![/bold green] Created root user:")
            console.print(new_user)
            # We return the user object here, but it's not strictly needed
            # by the CLI. It was part of the bug, so I'm leaving it.
            return new_user 
            
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")
    # 'finally' block is no longer needed, 'with' statement handles it.


@user.command(name="create")
def create_user() -> None:
    """
    Creates a new regular user.
    """
    console.print("[bold cyan]Creating New User...[/bold cyan]")
    email = "" # Define email here so it's available for error message
    
    try:
        with get_sync_client() as client:
            
            # --- THIS IS THE CORRECTED LOGIC ---
            # 1. Find the root user to act as the creator
            root_email = "rootadmin@todo.com"
            root_user = client.query_single(
                """
                WITH module user
                SELECT RootUser { id }
                FILTER .email = <str>$email
                LIMIT 1
                """,
                email=root_email,
            )

            # 2. Check if root user exists. If not, can't create users.
            if not root_user:
                console.print(f"[bold red]Root user not found. Please run 'cli user create-root' first.[/bold red]")
                return

            # 3. Create a NEW client instance with the global set
            # This ensures the AuditLog trigger knows who is making the change
            client_with_globals = client.with_globals(
                current_user_id=root_user.id
            )
            # --- END OF CORRECTION ---

            # Get user input
            email = Prompt.ask("Enter email")
            name = Prompt.ask("Enter name")
            phone_number = Prompt.ask("Enter phone number")
            password = Prompt.ask("Enter password", password=True)
            confirm_password = Prompt.ask("Confirm password", password=True)

            if password != confirm_password:
                console.print("[bold red]Passwords do not match. Aborting.[/bold red]")
                return

            # Hash the password
            hashed_password = hashpw(password.encode("utf-8"), gensalt())

            # Use the NEW client with the globals set
            # Insert User and Credential
            query = """
            WITH 
                module user,
                new_user := (
                    INSERT User {
                        email := <str>$email,
                        name := <str>$name,
                        phone_number := <str>$phone
                    }
                ),
                new_credential := (
                    INSERT Credential {
                        user := new_user,
                        password := <bytes>$password_hash
                    }
                )
            SELECT new_user {
                id,
                email,
                name,
                phone_number
            }
            """
            # Run the query using the client_with_globals
            new_user = client_with_globals.query_single(
                query,
                email=email,
                name=name,
                phone=phone_number,
                password_hash=hashed_password
            )
            
            console.print(f"[bold green]Success![/bold green] Created new user:")
            console.print(new_user)
        
    except ConstraintViolationError:
        console.print(f"[bold red]Error: A user with the email '{email}' already exists.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")
    # 'finally' block is no longer needed