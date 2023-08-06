from __future__ import annotations

from typing import Optional

from .kiota_client_factory import KiotaClientFactory


class KiotaClient:
    """Default httpx client with options and a middleware pipleline for requests execution.
    """
    __instance: Optional[KiotaClient] = None

    def __new__(cls, *args, **kwargs):
        if not KiotaClient.__instance:
            KiotaClient.__instance = object.__new__(cls)
        return KiotaClient.__instance

    def __init__(self) -> None:
        self.client = KiotaClientFactory().create_with_default_middleware()
