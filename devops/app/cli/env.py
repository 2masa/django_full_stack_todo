
import os
import secrets
import base64
import ipaddress
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
import rich_click as click
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa


console = Console()

def generate_b64_pwd(num_bytes=64):
    raw = secrets.token_bytes(num_bytes)
    return base64.b64encode(raw).decode()


def generate_cert_key(common_name, san, key_size, days_valid):
    # Generate private RSA key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)

    # Build certificate subject and issuer
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
    cert_builder = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=days_valid))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
    )

    # Add SANs if provided
    san_list = []
    for entry in san:
        try:
            san_list.append(x509.IPAddress(ipaddress.ip_address(entry)))
        except ValueError:
            san_list.append(x509.DNSName(entry))
    if san_list:
        cert_builder = cert_builder.add_extension(
            x509.SubjectAlternativeName(san_list), critical=False
        )

    # Sign the certificate
    cert = cert_builder.sign(private_key=private_key, algorithm=hashes.SHA256())

    # Serialize key and cert to PEM format
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)

    return key_pem, cert_pem

GEL_SERVER_TLS_KEY, GEL_SERVER_TLS_CERT = generate_cert_key(common_name="todo_app", san=["localhost", "172.0.0.3"], days_valid=365, key_size=4096)

GEL_SERVER_PASSWORD=generate_b64_pwd()

JWT_SECURITY_KEY=generate_b64_pwd()

DJANGO_SECURITY_KEY=generate_b64_pwd()

db_env = {
        "GEL_HOST":"172.0.0.3",
        "GEL_SERVER_USER":"todo",
        "GEL_SERVER_DEFAULT_BRANCH":"todo_branch",
        "GEL_SERVER_TLS_CERT_MODE":"require_file",
        "GEL_SERVER_PORT":"5151",
        "GEL_SERVER_TLS_CERT":GEL_SERVER_TLS_CERT.decode(),
        "GEL_SERVER_TLS_KEY":GEL_SERVER_TLS_KEY.decode(),
        "GEL_SERVER_PASSWORD":GEL_SERVER_PASSWORD,
        "GEL_SERVER_INSTANCE_NAME":"todo_instance"
    }
cli_env = db_env
cli_env.update({
        "DJANGO_PORT": 5000,
        "DJANGO_HOST": "0.0.0.0"})
env_data = {
    "db.env":db_env,
    "cli.env":cli_env,
    "api.env":{
        "JWT_SECURITY_ALGORITHM":"HS256",
        "JWT_TOKEN_TIMEOUT_MINUTES":60,
        "JWT_REFRESH_TOKEN_TIMEOUT_MINUTES":1440,
        "JWT_SECURITY_KEY": JWT_SECURITY_KEY,
    },  
    "ui.env":{
        "DJANGO_SECURITY_KEY": DJANGO_SECURITY_KEY,
        "FASTAPI_BASE_URL": "http://172.0.0.2:7000",
        "DJANGO_PORT": 5000,
        "DJANGO_HOST": "0.0.0.0",
        "DJANGO_DEBUG": "true",
        "REDIS_HOST": "172.0.0.5",
        "REDIS_PORT": 6379,
    },      
}

env_data["api.env"].update(db_env)
del env_data["api.env"]["GEL_SERVER_TLS_KEY"]


@click.group(name="env")
def env() -> None:
    """Environment file management commands."""
    pass


@env.command(name="create")
def create_env_files() -> None:
    """Create intelligent environment files"""
    successful_files = []
    failed_files = []
    
    console.rule("[bold magenta]Intelligent Environment File Creation[/bold magenta]")
    console.print(f"Attempting to create {len(env_data)} environment files...")

    # Ensure the envs directory exists
    os.makedirs("envs", exist_ok=True)

    for env_name in env_data:
        filepath = f"envs/{env_name}"
        
        try:
            with open(filepath, "w") as f:
                for key, value in env_data[env_name].items():
                    # CRITICAL FIX: Convert value to string before checking/writing
                    value_str = str(value) 

                    # For multiline values (like certs), quote and strip
                    if "\n" in value_str:
                        f.write(f'{key}="{value_str.strip()}"\n')
                    else:
                        f.write(f"{key}={value_str}\n") # Use the string version
            
            # Success feedback
            console.print(
                Text(f"[✓] Created: {filepath}", style="bold green")
            )
            successful_files.append(filepath)

        except IOError as e:
            # Error feedback
            console.print(
                Text(f"[X] FAILED to create: {filepath} ({e})", style="bold red")
            )
            failed_files.append(filepath)
        except Exception as e:
            # Catch unexpected errors
            console.print(
                Text(f"[!] UNEXPECTED ERROR during creation of: {filepath}", style="bold yellow")
            )
            console.print(f"    Details: {e}", style="yellow")
            failed_files.append(filepath)

    # Final Summary Panel
    console.rule("[bold magenta]Summary[/bold magenta]")
    
    # Success message based on outcome
    if successful_files and not failed_files:
        status_style = Style(color="white", bgcolor="green4", bold=True)
        status_text = "SUCCESS: All files created!"
    elif successful_files and failed_files:
        status_style = Style(color="black", bgcolor="yellow", bold=True)
        status_text = "PARTIAL SUCCESS: Some files failed."
    else:
        status_style = Style(color="white", bgcolor="red4", bold=True)
        status_text = "FAILURE: No files were created."

    summary_content = Text.assemble(
        Text(f"Status: ", style="bold"), Text(f"{status_text}\n", style=status_style),
        Text(f"Total files attempted: {len(env_data)}\n", style="cyan"),
        Text(f"Successful: {len(successful_files)}\n", style="green"),
        Text(f"Failed: {len(failed_files)}", style="red"),
    )
    
    console.print(Panel(summary_content, title="Creation Result", border_style="magenta"))

if __name__ == "__main__":
    # Example usage when running the script directly
    create_env_files()
