import re
from pathlib import Path
import typer
from enity.commands import (
    check as check_cmd,
    sync as sync_cmd,
    tidy as tidy_cmd,
    generate as generate_cmd,
    suggest_layout as suggest_layout_cmd,
)

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _read_version_from_pyproject() -> str:
    """
    Read the package version from pyproject.toml located at the repository root.

    This scans only the [project] table and looks for a `version = "x.y.z"` line.
    Falls back to "unknown" if reading/parsing fails.
    """
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except Exception:
        return "unknown"

    in_project = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            in_project = (s == "[project]")
            continue
        if in_project:
            m = re.match(r'version\s*=\s*["\'](.+?)["\']', s)
            if m:
                return m.group(1)
    return "unknown"


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", help="Show enity version and exit"),
):
    if version:
        typer.echo(_read_version_from_pyproject())
        raise typer.Exit()
    # No-op: allow subcommands or help to run/display when --version is not provided.


# Register the 'check' command directly to match CLI expectations/tests.
app.command("check")(check_cmd.check)
app.command("sync")(sync_cmd.run)
app.command("tidy")(tidy_cmd.run)
app.command("generate")(generate_cmd.run)
app.command("suggest-layout")(suggest_layout_cmd.suggest_layout)

if __name__ == "__main__":
    app()