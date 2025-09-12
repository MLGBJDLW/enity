# check.py
import json
import typer
from pathlib import Path
from enity.core.io import read_text, write_text
from enity.core.parser import keys_set_from_text
from enity.core.exceptions import EnityError
from enity.utils import console

# Command to check for missing or extra keys in .env file compared to .env.example
app = typer.Typer(help="Check for missing or extra keys in .env file compared to .env.example")

GITIGNORE_BLOCK = [
    "# Environments",
    ".env",
    ".env.*",
    "!.env.example",
]

def ensure_gitignore_rules(gitignore_path: Path) -> bool:
    """
    Ensure the project .gitignore contains the required env rules.
    Returns True if file was modified (rules appended), False if already conforms.
    """
    try:
        content = read_text(gitignore_path)
    except EnityError:
        # File missing or unreadable — treat as empty and create it
        content = ""

    # Normalize existing lines for comparison
    existing = {line.strip() for line in content.splitlines() if line.strip()}

    missing = [ln for ln in GITIGNORE_BLOCK if ln not in existing]

    if not missing:
        console.okay(".gitignore already contains required env ignore rules")
        return False

    # Prepare addition block, avoid duplicating blank lines
    addition_lines = GITIGNORE_BLOCK
    addition = ("\n" if content and not content.endswith("\n") else "") + "\n".join(addition_lines) + "\n"

    try:
        write_text(gitignore_path, content + addition)
        console.okay("Appended env ignore rules to .gitignore")
        return True
    except EnityError as e:
        console.error(f"Failed to update .gitignore: {e}")
        return False

# Command to check for missing or extra keys
@app.command()
def check(
    env_path: str = typer.Option(".env", "--env", "-e", help="Path to the .env file"),
    example_path: str = typer.Option(".env.example", "--example", "-x", help="Path to the .env.example file"),
    only: str = typer.Option("all", help="Check only for 'missing' keys, 'extra' keys, or 'all' keys"),
    strict_extra: bool = typer.Option(True, help="Treat extra keys as errors (exit non-zero)"),
    format: str = typer.Option("text", "--format", "-f", help="Output format: 'text' or 'json'"),
):
    """
    Compare keys between an .env file and an .env.example file.

    Note: `only` accepts 'all', 'missing', or 'extra'. We avoid using typing.Literal
    because some Typer versions have limited support for Literal annotations.
    """
    env_p = Path(env_path)
    example_p = Path(example_path)

    # Validate the 'only' option
    if only not in {"all", "missing", "extra"}:
        typer.echo(f"Invalid value for --only: {only}")
        raise typer.Exit(code=2)

    try:
        env_text = read_text(env_p)
        ex_text = read_text(example_p)
    except EnityError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    env_keys = keys_set_from_text(env_text)
    ex_keys = keys_set_from_text(ex_text)

    missing = ex_keys - env_keys
    extra = env_keys - ex_keys

    # Apply 'only' filter
    if only == "missing":
        extra = set()
    elif only == "extra":
        missing = set()

    if format == "json":
        payload = {
            "env": str(env_p.resolve()),
            "example": str(example_p.resolve()),
            "missing": sorted(missing),
            "extra": sorted(extra),
            "okay": len(missing) == 0 and (not strict_extra or len(extra) == 0),
        }
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=4))
    else:
        # Text output matching tests' expectations
        if not missing and not extra:
            # Tests look for "OK" in output
            typer.echo("OK")
        else:
            if missing:
                # Print filename (basename) like the tests expect
                typer.echo(f"Missing keys in {env_p.name}: {missing}")
            if extra:
                typer.echo(f"Extra keys in {env_p.name}: {extra}")

    # Ensure .gitignore in project root has the env rules.
    gitignore_path = Path.cwd() / ".gitignore"
    ensure_gitignore_rules(gitignore_path)

    # Exit codes: tests expect 1 for missing/extra, 0 for success
    if missing or (extra and strict_extra):
        raise typer.Exit(code=1)
    else:
        raise typer.Exit(code=0)