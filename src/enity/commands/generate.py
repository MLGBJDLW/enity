import typer
from pathlib import Path
import re

def generate_file(env_file: Path, example_file: Path, force: bool = False) -> None:
    """
    Core generation logic: produce an .env.example from env_file.
    Raises exceptions on failure; does not call typer.Exit so it can be reused.
    """
    if not env_file.exists():
        raise FileNotFoundError(f"Input file not found at '{env_file}'")

    if example_file.exists() and not force:
        raise FileExistsError(f"Output file '{example_file}' already exists. Use --force to overwrite.")

    content = env_file.read_text()
    # Use regex to find lines like KEY=... and replace them with KEY=
    # This preserves comments, blank lines, and ordering.
    generated_content = re.sub(r"^(?!#)([^=]+)=.*$", r"\1=", content, flags=re.MULTILINE)

    try:
        example_file.write_text(generated_content)
    except IOError as e:
        raise IOError(f"Error writing to file '{example_file}': {e}")


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
    This CLI wrapper uses the reusable `generate_file` core function.
    """
    try:
        generate_file(env_file, example_file, force=force)
        print(f"Successfully generated '{example_file}' from '{env_file}'.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)
    except FileExistsError as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)

    raise typer.Exit(code=0)