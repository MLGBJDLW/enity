# config.py
from pathlib import Path
from typing import Dict, Tuple, Optional, Union

# Try to use stdlib tomllib (Py3.11+), fall back to 'toml' package if unavailable.
try:
    import tomllib as _toml  # type: ignore
except Exception:
    import toml as _toml  # type: ignore

_DEFAULTS = {"env_path": ".env", "example_path": ".env.example"}


def _load_pyproject(path: Path) -> Dict:
    if not path.exists():
        return {}
    # tomllib wants binary mode, toml lib wants text mode; try binary first.
    try:
        with path.open("rb") as f:
            data = _toml.load(f)
    except Exception:
        with path.open("r", encoding="utf-8") as f:
            data = _toml.load(f)
    return data.get("tool", {}).get("enity", {})


# Load config from the project's pyproject.toml located at CWD/pyproject.toml
_cfg = _load_pyproject(Path.cwd() / "pyproject.toml")

ENV_PATH: str = _cfg.get("env_path", _DEFAULTS["env_path"])
EXAMPLE_PATH: str = _cfg.get("example_path", _DEFAULTS["example_path"])


def get_env_paths() -> Tuple[str, str]:
    """Return (env_path, example_path) from loaded config or defaults."""
    return ENV_PATH, EXAMPLE_PATH


def reload(path: Optional[Union[str, Path]] = None) -> None:
    """Reload configuration from a specific pyproject.toml path or CWD/pyproject.toml."""
    p = Path(path) if path else Path.cwd() / "pyproject.toml"
    global _cfg, ENV_PATH, EXAMPLE_PATH
    _cfg = _load_pyproject(p)
    ENV_PATH = _cfg.get("env_path", _DEFAULTS["env_path"])
    EXAMPLE_PATH = _cfg.get("example_path", _DEFAULTS["example_path"])