import logging

from meili_sdk.clients.base import BaseAPIClient

__all__ = ("APITokenClient",)

logger = logging.getLogger("meili")


class APITokenClient(BaseAPIClient):
    AUTHORIZATION_TOKEN_HEADER = "Token"  # nosec

    def __init__(self, *args, **kwargs):
        logging.warning(
            "This client is about to be deprecated, please use PersistentTokenClient instead"
        )
        super().__init__(*args, **kwargs)
