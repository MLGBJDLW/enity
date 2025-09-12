import typer
from pathlib import Path
from enity.core.parser import keys_set_from_text

def run(
    env_file: Path = typer.Option(
        ".env", "--env", "-e", help="Path to the .env file to update."
    ),
    example_file: Path = typer.Option(
        ".env.example", "--example", "-x", help="Path to the .env.example file to read from."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be changed without modifying the file."
    ),
):
    """
    Add missing variables from .env.example to .env.
    """
    if not example_file.exists():
        print(f"Error: Example file not found at '{example_file}'")
        raise typer.Exit(code=1)

    env_content = env_file.read_text() if env_file.exists() else ""
    example_content = example_file.read_text()

    env_keys = keys_set_from_text(env_content)
    example_keys = keys_set_from_text(example_content)

    missing_keys = example_keys - env_keys

    if not missing_keys:
        print("OK: .env file is already in sync with .env.example.")
        raise typer.Exit(code=0)

    if dry_run:
        print("--- .env (dry run) ---")
        print(f"Would add the following missing keys: {sorted(list(missing_keys))}")
        raise typer.Exit(code=0)

    # Append missing keys to the .env file content
    new_env_content = env_content.strip()
    if new_env_content:
        new_env_content += "\n\n" # Add separator if file is not empty
        
    new_env_content += "# Added by enity sync\n"
    new_env_content += "\n".join(f"{key}=" for key in sorted(list(missing_keys)))
    new_env_content += "\n"

    try:
        env_file.write_text(new_env_content)
        print(f"Successfully added {len(missing_keys)} missing keys to '{env_file}'.")
    except IOError as e:
        print(f"Error writing to file '{env_file}': {e}")
        raise typer.Exit(code=1)