import typer
from pathlib import Path
import re

def run(
    env_file: Path = typer.Option(
        ".env", "--env", "-e", help="Path to the input .env file."
    ),
    example_file: Path = typer.Option(
        ".env.example", "--example", "-x", help="Path to the output .env.example file."
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force overwrite if the example file already exists."
    ),
):
    """
    Generate an .env.example file from an .env file.
    """
    if not env_file.exists():
        print(f"Error: Input file not found at '{env_file}'")
        raise typer.Exit(code=1)

    if example_file.exists() and not force:
        print(f"Error: Output file '{example_file}' already exists. Use --force to overwrite.")
        raise typer.Exit(code=1)

    content = env_file.read_text()
    # Use regex to find lines like KEY=... and replace them with KEY=
    # This preserves comments, blank lines, and ordering.
    generated_content = re.sub(r"^(?!#)([^=]+)=.*$", r"\1=", content, flags=re.MULTILINE)

    try:
        example_file.write_text(generated_content)
        print(f"Successfully generated '{example_file}' from '{env_file}'.")
    except IOError as e:
        print(f"Error writing to file '{example_file}': {e}")
        raise typer.Exit(code=1)

    raise typer.Exit(code=0)