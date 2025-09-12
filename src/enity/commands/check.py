# check.py
import json
import typer
from pathlib import Path
from typing import Literal
from enity.core.io import read_text
from enity.core.parser import keys_set_from_text
from enity.utils.console import okay, error, warn
from enity.core.exceptions import EnityError

# Command to check for missing or extra keys in .env file compared to .env.example
app = typer.Typer(help = 'Check for missing or extra keys in .env file compared to .env.example')

# Command to check for missing or extra keys
@app.command()
def check(
    env_path: str = typer.Option(".env", help="Path to the .env file"),
    example_path: str = typer.Option(".env.example", help="Path to the .env.example file"),
    only: Literal["all", "missing", "extra"] = typer.Option("all", help="Check only for 'missing' keys, 'extra' keys, or 'all' keys"),
    strict_extra: bool = typer.Option(True, help="Treat extra keys as errors (exit non-zero)"),
    format: Literal["text", "json"] = typer.Option("text", help="Output format: 'text' or 'json'"),
):
    env_p = Path(env_path)
    example_p = Path(example_path)

    try:
        env_text = read_text(env_p)
        ex_text = read_text(example_p)
    except EnityError as e:
        error(f"Error: {e}")
        raise typer.Exit(code=1)
        

    env_keys = keys_set_from_text(env_text)
    ex_keys = keys_set_from_text(ex_text)

    missing = ex_keys - env_keys
    extra = env_keys - ex_keys
    
    # Prepare results based on the 'only' option
    if only == "missing":
        extra = []
    elif only == "extra":
        missing = []
        
    if format == "json":
        payload = {
            "env": str(str(env_p.resolve())),
            "example": str(str(example_p.resolve())),
            "missing": sorted(missing),
            "extra": sorted(extra),
            "okay": len(missing) == 0 and (not strict_extra or len(extra) == 0)
        }
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=4))
    else:
        if not missing and not extra:
            okay(f"{env_p} is in sync with {example_p}. No missing or extra keys.")
        else:
            if missing:
                warn(f"Missing keys in {env_p} (present in {example_p}):")
                for k in missing:
                    typer.echo(f"  - {k}")
            if extra:
                warn(f"Extra keys in {env_p} (not present in {example_p}):")
                for k in extra:
                    typer.echo(f"  - {k}")
    
    # Exit with appropriate code
    if missing or (extra and strict_extra):
        raise typer.Exit(code=2)
    else:
        raise typer.Exit(code=0)