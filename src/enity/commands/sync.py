# sync.py
import json
import time
import typer
from pathlib import Path
from typing import Literal
from enity.core.io import read_text, write_text
from enity.core.parser import keys_set_from_text
from enity.utils.console import okay, error, warn
from enity.core.exceptions import EnityError

# Command to sync .env file with .env.example
app = typer.Typer(help='Sync .env file with .env.example by adding missing keys and optionally removing extra keys')

# Time stamp for backup files
def _timestamp():
    return time.strftime("%Y%m%d%H%M%S")

# Command to sync .env file with .env.example
@app.command()
def sync(
    env_path: str = typer.Option(".env", help="Path to the .env file"),
    example_path: str = typer.Option(".env.example", help="Path to the .env.example file"),
    assume_empty: bool = typer.Option(False, help="Do not prompt; fill missing keys with empty values"),
    dry_run: bool = typer.Option(False, help="Show changes without modifying the .env file"),
    backup: bool = typer.Option(True, help="Create a backup of the .env file before modifying"),
    format: Literal["text", "json"] = typer.Option("text", help="Output format: 'text' or 'json'"),
):
    env_p = Path(env_path)
    example_p = Path(example_path)

    try:
        env_text = env_p.read_text(encoding="utf-8") if env_p.exists() else ""
        ex_text = read_text(example_p)
    except EnityError as e:
        error(f"Error: {e}")
        raise typer.Exit(code=1)

    env_keys = keys_set_from_text(env_text)
    ex_keys = keys_set_from_text(ex_text)

    missing = [k for k in ex_keys if k not in env_keys]
    additions: list[str] = []
    planned_values: dict[str, str] = {}

    if missing and not assume_empty and not dry_run:
        for k in missing:
            val = typer.prompt(f"Enter value for missing key '{k}' (leave empty for no value)", default="")
            planned_values[k] = val
            additions.append(f"{k}={val}")
    elif missing:
        # Fill missing keys with empty values
        for k in missing:
            planned_values[k] = ""
            additions.append(f"{k}=")

    # Output results
    if format == "json":
        payload = {
            "env": str(env_p.resolve()),
            "example": str(example_p.resolve()),
            "missing": missing,
            "planned_values": planned_values,
            "will_write": (len(additions) > 0 and not dry_run),
        }
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=4))
    else:
        if not missing:
            okay("No missing keys. .env is in sync with .env.example.")
        else:
            warn(f"Missing {len(missing)} keys will be added to {env_p}:")
            for k in missing:
                typer.echo(f"  - {k} (value: '{planned_values[k]}')")

            if dry_run:
                warn("Dry run enabled; no changes will be made to the .env file.")
            else:
                if assume_empty:
                    warn("Assume empty enabled; missing keys will be added with empty values.")


    # Write changes to .env file if not a dry run
    if additions and not dry_run:
        if backup and env_p.exists():
            bak = env_p.with_suffix(env_p.suffix + f".bak.{_timestamp()}")
            bak.write_text(env_text, encoding="utf-8")
            okay(f"Backup of .env created at {bak}")
        sep = "\n" if env_text and not env_text.endswith("\n") else ""
        write_text(env_p, env_text + sep + "\n".join(additions) + "\n")
        okay(f"Added {len(additions)} missing keys to {env_p}.")

    # Exit with appropriate code
    if missing and dry_run:
        raise typer.Exit(code=2)
    else:
        raise typer.Exit(code=0)