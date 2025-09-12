import typer
from enity.commands import (
    check as check_cmd,
    sync as sync_cmd,
    tidy as tidy_cmd,
    generate as generate_cmd,
)

app = typer.Typer(no_args_is_help=True, add_completion=False)

# Register the 'check' command directly to match CLI expectations/tests.
app.command("check")(check_cmd.check)
app.command("sync")(sync_cmd.run)
app.command("tidy")(tidy_cmd.run)
app.command("generate")(generate_cmd.run)

if __name__ == "__main__":
    app()