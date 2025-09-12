import re
from typing import List, Set
from enity.core.exceptions import EnityError, FileParsingError

# Regular expression to match lines with KEY=VALUE format
LINE_KEY_RE = re.compile(r"^\s*([A-Z0-9_]+)\s*=", re.MULTILINE)

def extract_keys_from_text(content: str) -> List[str]:
    """Extracts unique keys from the given text content."""
    if not isinstance(content, str):
        raise FileParsingError("Content must be a string")
    try:
        keys: List[str] = []
        for line in content.splitlines():
            match = re.match(LINE_KEY_RE, line)
            if match:
                keys.append(match.group(1))
        return keys
    except Exception as e:
        raise FileParsingError(f"Failed to extract keys from content: {e}") from e

def keys_set_from_text(content: str) -> Set[str]:
    """Extracts a set of unique keys from the given text content."""
    try:
        return set(extract_keys_from_text(content))
    except EnityError:
        # Re-raise domain exceptions as-is
        raise
    except Exception as e:
        raise FileParsingError(f"Failed to build keys set: {e}") from e