"""Exceptions used in the package."""


class APIRequestException(Exception):
    """Exception raised when an API request fails."""

    def __init__(self, url: str, response: dict):
        super().__init__(f"Request to '{url}' failed. Response: {response}")


class EmptyDataFrameException(Exception):
    """Exception raised when the DataFrame is empty."""

    def __init__(self):
        super().__init__("DataFrame is empty.")


class NonUniquePrimaryKeyException(Exception):
    """Exception raised when the primary key is not unique."""

    def __init__(self, column_name: str):
        super().__init__(
            f"The '{column_name}' has non unique values. Primary key check failed."
        )


class NullValuesFoundException(Exception):
    """Exception raised when null values are found in the DataFrame."""

    def __init__(self):
        super().__init__("Null values found in the DataFrame.")
