import typer
from pathlib import Path

def run(
    env_file: Path = typer.Option(
        ".env", "--env", "-e", help="Path to the .env file to tidy."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be changed without modifying the file."
    ),
):
    """
    Sort the keys in an .env file.
    """
    if not env_file.exists():
        print(f"Error: File not found at '{env_file}'")
        raise typer.Exit(code=1)

    lines = env_file.read_text().splitlines()
    
    variables = [line for line in lines if "=" in line and not line.strip().startswith("#")]
    other_lines = [line for line in lines if "=" not in line or line.strip().startswith("#")]
    
    sorted_variables = sorted(variables)

    if sorted_variables == variables:
        print(f"OK: '{env_file}' is already tidy.")
        raise typer.Exit(code=0)

    new_content = "\n".join(other_lines + sorted_variables) + "\n"

    if dry_run:
        print("--- .env (dry run) ---")
        print("Original variables order:")
        print("\n".join(variables))
        print("\nTidied variables order:")
        print("\n".join(sorted_variables))
        raise typer.Exit(code=0)

    try:
        env_file.write_text(new_content)
        print(f"Successfully tidied '{env_file}'.")
    except IOError as e:
        print(f"Error writing to file '{env_file}': {e}")
        raise typer.Exit(code=1)