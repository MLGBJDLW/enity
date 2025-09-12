import typer
from pathlib import Path
from typing import List, Tuple, Optional
from enity.core import io as core_io

def compute_tidy(content: str) -> Tuple[List[str], List[str], str]:
    """
    Compute tidied variables and resulting content from the raw .env content.
    Returns (original_variables, sorted_variables, new_content).
    """
    lines = content.splitlines()
    variables = [line for line in lines if "=" in line and not line.strip().startswith("#")]
    other_lines = [line for line in lines if "=" not in line or line.strip().startswith("#")]
    sorted_variables = sorted(variables)
    new_content = "\n".join(other_lines + sorted_variables) + "\n"
    return variables, sorted_variables, new_content

def tidy_file(env_file: Path, write: bool = True, dry_run: bool = False) -> Optional[str]:
    """
    Tidy the given env_file. If write is False, do not persist changes.
    Returns the new content if changes would be/ were made, otherwise None.
    """
    try:
        content = core_io.read_text(env_file)
    except Exception:
        # Let caller handle missing file or IO errors
        raise

    variables, sorted_variables, new_content = compute_tidy(content)

    if sorted_variables == variables:
        # Nothing to do
        return None

    if dry_run:
        # Do not write, just return new content for inspection
        return new_content

    if write:
        core_io.write_text(env_file, new_content)
    return new_content

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

    try:
        content = core_io.read_text(env_file)
    except Exception as e:
        print(f"Error reading file '{env_file}': {e}")
        raise typer.Exit(code=1)

    variables, sorted_variables, new_content = compute_tidy(content)

    if sorted_variables == variables:
        print(f"OK: '{env_file}' is already tidy.")
        raise typer.Exit(code=0)

    if dry_run:
        print("--- .env (dry run) ---")
        print("Original variables order:")
        print("\n".join(variables))
        print("\nTidied variables order:")
        print("\n".join(sorted_variables))
        raise typer.Exit(code=0)

    try:
        core_io.write_text(env_file, new_content)
        print(f"Successfully tidied '{env_file}'.")
    except Exception as e:
        print(f"Error writing to file '{env_file}': {e}")
        raise typer.Exit(code=1)