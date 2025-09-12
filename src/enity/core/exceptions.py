class EnityError(Exception):
    """Base exception for all enity errors."""


class FileNotFoundError(EnityError):
    """Raised when a file is not found."""


class FileParsingError(EnityError):
    """Raised when a file cannot be parsed."""