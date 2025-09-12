import typer

# Utility functions for console output with colored messages
def okay(message: str):
    typer.secho(f"✅ {message}", fg=typer.colors.GREEN)
    
def error(message: str):
    typer.secho(f"❌ {message}", fg=typer.colors.RED, err=True)
    
def warn(message: str):
    typer.secho(f"⚠️ {message}", fg=typer.colors.YELLOW)
