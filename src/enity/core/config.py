# config.py
from pathlib import Path
from typing import Dict, Tuple, Optional, Union, List

# Try to use stdlib tomllib (Py3.11+), fall back to 'toml' package if unavailable.
try:
    import tomllib as _toml  # type: ignore
except Exception:
    import toml as _toml  # type: ignore

import tomli  # type: ignore
from pydantic import BaseModel, Field

_DEFAULTS = {"env_path": ".env", "example_path": ".env.example"}


class GroupingRule(BaseModel):
    name: str
    keywords: List[str] = Field(default_factory=list)
    prefixes: List[str] = Field(default_factory=list)


class Config(BaseModel):
    grouping_rules: Optional[Dict[str, GroupingRule]] = None


def load_config() -> Optional[Config]:
    """Load and validate .enity.toml from the project root.

    Returns a Config instance when the file exists and parses correctly.
    Returns an empty Config() when file missing or on parse/validation error.
    """
    p = Path.cwd() / ".enity.toml"
    if not p.exists():
        return Config()
    try:
        with p.open("rb") as f:
            data = tomli.load(f)
        # Pass top-level mapping to pydantic model
        return Config(**data)
    except Exception as e:
        # Non-fatal: warn and return empty Config
        print(f"Warning: Failed to load .enity.toml: {e}")
        return Config()


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