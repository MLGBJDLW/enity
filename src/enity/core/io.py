from pathlib import Path
from enity.core.exceptions import EnityError, FileNotFoundError

def read_text(path: Path) -> str:
    """
    Read text from path. On missing file raise FileNotFoundError (EnityError subclass).
    Other IO errors are wrapped in EnityError.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        raise EnityError(f"Failed to read file {path}: {e}") from e

def write_text(path: Path, content: str) -> None:
    try:
        path.write_text(content, encoding="utf-8")
    except Exception as e:
        raise EnityError(f"Failed to write file {path}: {e}") from e