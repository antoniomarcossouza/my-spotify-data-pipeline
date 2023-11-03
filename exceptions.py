class APIRequestException(Exception):
    """Exception raised when an API request fails."""

    def __init__(self, url: str, response: dict):
        super().__init__(f"Request to '{url}' failed. Response: {response}")
