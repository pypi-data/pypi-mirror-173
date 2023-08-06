"""Data Models for XRTC: connection, login, set/get API. Pydantic is used for parsing."""
from pydantic import BaseSettings, BaseModel, Field


class ConnectionConfiguration(BaseSettings):
    """Connection configuration"""

    # Connection URL
    login_url: str = Field("https://api.xrtc.org/v1/auth/login", env="LOGIN_URL")
    set_url: str = Field("https://api.xrtc.org/v1/item/set", env="SET_URL")
    get_url: str = Field("https://api.xrtc.org/v1/item/get", env="GET_URL")

    # Default timeouts and connection limits

    # Duration of the whole operation incl connection establishment, request sending & response reading, seconds
    timeout_total: int = 20

    # Duration of new connection or for waiting for a free connection from a pool if limits are exceeded, seconds
    timeout_connect: float = 5

    # Duration of connecting to a peer for a new connection, not given from a pool, seconds
    timeout_sock_connect: float = 5

    # Duration of the period between reading a new data portion from a peer, seconds
    timeout_sock_read: float = 10

    # Duration of the DNS entries expiry, seconds
    timeout_dns_cache: int = 300

    # Total number simultaneous connections to any hosts
    limit_connections: int = 100

    # Total number of concurrent requests
    limit_concurrent_requests: int = 5

    class Config:
        """Read configuration from default .env"""

        env_file = "xrtc.env"


class LoginCredentials(BaseSettings):
    """Loging configuration"""

    accountid: int = Field(..., env="ACCOUNT_ID")
    apikey: str = Field(..., env="API_KEY")

    class Config:
        """Read configuration from default .env"""

        env_file = "xrtc.env"


class Item(BaseModel):
    """Data model for API element Item"""

    portalid: str
    payload: str
    servertimestamp: int = 0


class Portal(BaseModel):
    """Data model for API element Portal"""

    portalid: str
    servertimestamp: int = 0


class SetItemRequest(BaseModel):
    """Data model for API request item/set"""

    items: list[Item]


class GetItemRequest(BaseModel):
    """Data model for API request item/get"""

    portals: list[Portal] = None
    polling: int = 0


class ReceivedData(BaseModel):
    """Data model for API response item/get"""

    items: list[Item] = None


class Error(BaseModel):
    """Data model for API response item/get"""

    errorgroup: int = 0
    errorcode: int = 0
    errormessage: str = None


class ReceivedError(BaseModel):
    """Data model for API response item/get"""

    error: Error = None
