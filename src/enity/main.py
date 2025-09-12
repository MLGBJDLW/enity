# main.py
import typer
from enity.commands.check import check
from enity.commands.tidy import tidy
from enity.commands.sync import sync

app = typer.Typer(help="Environment File Management Tool")
app.add_typer(check, name="check", help="Check for missing or extra keys in .env file compared to .env.example")
app.add_typer(tidy, name="tidy", help="Tidy .env file according to .env.example")
app.add_typer(sync, name="sync", help="Sync .env file with .env.example by adding missing keys and optionally removing extra keys")

if __name__ == "__main__":
    app()