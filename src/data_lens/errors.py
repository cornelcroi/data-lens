class DataLensError(Exception):
    """Base exception for Data Lens errors."""
    pass


class UnsafeQueryError(DataLensError):
    """Raised when a SQL query contains unsafe operations."""
    pass


class FileLoadError(DataLensError):
    """Raised when file loading fails."""
    pass


class UnsupportedFormatError(FileLoadError):
    """Raised when file format is not supported."""
    pass


class QueryExecutionError(DataLensError):
    """Raised when SQL query execution fails."""
    pass


class TableNotFoundError(DataLensError):
    """Raised when referenced table doesn't exist."""
    pass
