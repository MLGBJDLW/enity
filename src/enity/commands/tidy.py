# tidy.py
import json
import difflib
import time
import re
import typer
from pathlib import Path
from typing import Literal
from enity.core.io import read_text, write_text
from enity.utils.console import okay, warn, error
from enity.core.config import ENV_PATH, EXAMPLE_PATH

# Command to tidy .env file according to .env.example
app = typer.Typer(help='Tidy .env file according to .env.example by sorting keys and removing duplicates')

KEY_LINE_RE = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$')

# Time stamp for backup files
def _timestamp() -> str:
    return time.strftime("%Y%m%d%H%M%S")

def _kv_map(text: str) -> dict[str, str]:
    kv: dict[str, str] = {}
    for line in text.splitlines():
        match = KEY_LINE_RE.match(line)
        if match:
            key = match.group(1)
            val = match.group(2)
            kv[key] = val
    return kv

# Command to tidy .env file according to .env.example
@app.command()
def tidy(
    env_path: str = typer.Option(ENV_PATH, help="Path to .env"),
    example_path: str = typer.Option(EXAMPLE_PATH, help="Path to .env.example"),
    remove_ghosts: bool = typer.Option(True, help="Drop keys not present in template"),
    append_ghosts_at_end: bool = typer.Option(
        False, help="If not removing ghosts, append them at the end with # ghost tag"
    ),
    check: bool = typer.Option(
        False, help="Check-only mode: exit 2 if changes would be made"
    ),
    dry_run: bool = typer.Option(False, help="Show diff, do not write"),
    backup: bool = typer.Option(True, help="Create a timestamped backup before writing"),
    format: Literal["text", "json"] = typer.Option("text", help="Output format"),
):

    env_p = Path(env_path)
    ex_p = Path(example_path)

    try:
        env_text = read_text(env_p)
        ex_text = read_text(ex_p)
    except FileNotFoundError:
        raise typer.Exit(code=1)

    env_kv = _kv_map(env_text)
    out_line: list[str] = []
    seen: set[str] = set()

    # Process example file to determine order
    for line in ex_text.splitlines():
        match = KEY_LINE_RE.match(line)
        if match:
            key = match.group(1)
            if key in env_kv and key not in seen:
                out_line.append(f"{key}={env_kv[key]}")
                seen.add(key)
            elif key not in seen:
                out_line.append(line)  # Keep as is from example
                seen.add(key)
        else:
            out_line.append(line)  # Non-key lines are copied as is

    # Handle ghost keys
    ghosts = [k for k in env_kv.keys() if k not in seen]

    if not remove_ghosts and ghosts:
        if append_ghosts_at_end:
            out_line.append("")  # Blank line before ghosts
            for g in ghosts:
                out_line.append(f"{g}={env_kv[g]}  # ghost")
        else:
            for g in ghosts:
                out_line.append(f"{g}={env_kv[g]}")

    new_env_text = "\n".join(out_line).rstrip() + "\n"

    changed = (new_env_text != env_text)

    if format == "json":
        payload = {
            "env": str(env_p.resolve()),
            "example": str(ex_p.resolve()),
            "changed": changed,
            "ghosts": ghosts,
            "remove_ghosts": remove_ghosts,
        }
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=4))

    else:
        if not changed:
            okay(f"{env_p} is already tidy and in sync with {ex_p}. No changes made.")
        else:
            warn(f"{env_p} is not tidy or not in sync with {ex_p}. Changes will be made.")

            # Show diff
            diff = difflib.unified_diff(
                env_text.splitlines(),
                new_env_text.splitlines(),
                fromfile=str(env_p),
                tofile=str(env_p) + " (tidied)",
                lineterm="",
            )
            for line in diff:
                typer.echo(line)

            if dry_run or check:
                warn("Dry run enabled; no changes will be made to the .env file.")

    # Write changes if not dry run or check
    if changed and not (dry_run or check):
        if backup and env_p.exists():
            bak = env_p.with_suffix(env_p.suffix + f".bak.{_timestamp()}")
            bak.write_text(env_text, encoding="utf-8")
            okay(f"Backup of .env created at {bak}")
        write_text(env_p, new_env_text)
        okay(f"Wrote tidied .env -> {env_p}.")

    # Exit with appropriate code
    if changed and (dry_run or check):
        raise typer.Exit(code=2)
    else:
        raise typer.Exit(code=0)