import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Iterable

import typer

from enity.core import io as core_io
from enity.core import parser as core_parser
from enity.commands import tidy as tidy_cmd, generate as generate_cmd


def _parse_env_text(content: str) -> Dict[str, str]:
    """Parse simple env-style KEY=VALUE lines from text."""
    result: Dict[str, str] = {}
    for raw in content.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        if key:
            result[key] = val
    return result


def _parse_json_text(content: str) -> Dict[str, str]:
    """Parse JSON mapping of keys to values."""
    try:
        data = json.loads(content)
    except Exception as e:
        raise ValueError(f"Invalid JSON: {e}")
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object mapping keys to values")
    return {str(k): "" if v is None else str(v) for k, v in data.items()}


def _read_input(from_file: Optional[Path]) -> str:
    """Read input either from a file or from stdin."""
    if from_file:
        return core_io.read_text(from_file)
    # Read entire stdin
    return sys.stdin.read()


def _replace_or_append_env(content: str, updates: Dict[str, str]) -> str:
    """
    Given existing .env content and updates mapping, produce updated content.
    - Replace values for existing keys
    - Append new KEY=VALUE lines for keys not present
    Preserve non-key lines (comments, blank lines) in their positions.
    """
    lines = content.splitlines()
    key_re = core_parser.LINE_KEY_RE
    updated_keys = set()
    out_lines = []

    for line in lines:
        m = key_re.match(line)
        if m:
            key = m.group(1)
            if key in updates:
                out_lines.append(f"{key}={updates[key]}")
                updated_keys.add(key)
            else:
                out_lines.append(line)
        else:
            out_lines.append(line)

    # Append new keys that were not present
    for k, v in updates.items():
        if k not in updated_keys:
            out_lines.append(f"{k}={v}")

    return "\n".join(out_lines) + ("\n" if out_lines else "")


def _ensure_example_has_keys(example_content: str, keys: Iterable[str]) -> str:
    """
    Ensure that each key in keys appears in the .env.example content.
    Missing keys will be appended with empty values (KEY=).
    """
    existing = set(core_parser.keys_set_from_text(example_content) if example_content else set())
    lines = example_content.splitlines() if example_content else []
    to_add = [k for k in keys if k not in existing]

    if not to_add:
        return example_content

    # Ensure a trailing blank line separation before appending if file not empty
    if lines and lines[-1].strip() != "":
        lines.append("")

    for k in to_add:
        lines.append(f"{k}=")

    return "\n".join(lines) + ("\n" if lines else "")


def run(
    from_file: Optional[Path] = typer.Option(
        None, "--from-file", "-f", help="Path to file to load variables from (defaults to stdin)."
    ),
    format: str = typer.Option("env", "--format", "-t", help="Input format: env or json"),
):
    """
    Load variables from a file or stdin into .env, update .env.example (add new keys with empty values),
    and run tidy to normalize the .env file.
    """
    fmt = (format or "env").lower()
    if fmt not in ("env", "json"):
        typer.echo("Error: --format must be 'env' or 'json'")
        raise typer.Exit(code=1)

    try:
        raw = _read_input(from_file)
    except Exception as e:
        typer.echo(f"Error reading input: {e}")
        raise typer.Exit(code=1)

    try:
        updates = _parse_env_text(raw) if fmt == "env" else _parse_json_text(raw)
    except Exception as e:
        typer.echo(f"Error parsing input: {e}")
        raise typer.Exit(code=1)

    if not updates:
        typer.echo("No variables found in input.")
        raise typer.Exit(code=0)

    env_path = Path(".env")
    example_path = Path(".env.example")

    # Read existing .env (if missing, treat as empty)
    try:
        env_content = core_io.read_text(env_path)
    except Exception:
        env_content = ""

    new_env_content = _replace_or_append_env(env_content, updates)

    try:
        core_io.write_text(env_path, new_env_content)
    except Exception as e:
        typer.echo(f"Error writing .env: {e}")
        raise typer.Exit(code=1)

    # Update .env.example to include newly added keys with empty values
    try:
        try:
            example_content = core_io.read_text(example_path)
        except Exception:
            example_content = ""
        updated_example = _ensure_example_has_keys(example_content, updates.keys())
        if updated_example != example_content:
            core_io.write_text(example_path, updated_example)
    except Exception as e:
        typer.echo(f"Error updating .env.example: {e}")
        raise typer.Exit(code=1)

    # Run tidy logic to normalize/sort .env
    try:
        tidy_cmd.tidy_file(env_path, write=True, dry_run=False)
    except Exception as e:
        typer.echo(f"Error tidying .env: {e}")
        raise typer.Exit(code=1)

    # Run generate logic to (re)generate declarations in .env.example based on .env
    try:
        # Use the core function from generate module; do not force overwrite
        generate_cmd.generate_file(env_path, example_path, force=False)
    except Exception as e:
        typer.echo(f"Error generating .env.example: {e}")
        raise typer.Exit(code=1)

    typer.echo("Loaded variables into .env, synchronized .env.example, tidied .env, and regenerated .env.example declarations.")