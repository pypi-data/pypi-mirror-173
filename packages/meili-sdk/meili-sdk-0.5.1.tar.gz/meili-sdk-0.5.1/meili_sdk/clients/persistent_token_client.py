from meili_sdk.clients.base import BaseAPIClient
from meili_sdk.resources.ros import RosSetupResource

__all__ = ("PersistentTokenClient",)


class PersistentTokenClient(BaseAPIClient):
    AUTHORIZATION_TOKEN_HEADER = "API-Key"  # nosec

    def get_ros_resources(self):
        return RosSetupResource(self)
