"""Context manager (non-async) for XRTC: login and set/get API."""


import requests


from xrtc import (
    LoginCredentials,
    ConnectionConfiguration,
    ReceivedError,
    GetItemRequest,
    SetItemRequest,
    ReceivedData,
    XRTCException,
)


class XRTC:
    """Context manager (non-async) for XRTC: login and set/get API."""

    def __init__(self, env_file_credentials: str = None, env_file_connection: str = None):
        """
        Initialize connection and credentials.

        Connection credentials and URLs can be specified in .env files. If the file name does not contain the full path,
        then the work directory is assumed. If the file names are not specified, then "xrtc.env" is used by default.
        The values in the files are overridden by environmental variables.

        Parameters:
            env_file_credentials (str): .env file with connection credentials (account id, API key).
            env_file_connection (str): .env file with connection URLs (login, set and get item).
        """
        # Get credentials from .env file
        if env_file_credentials is not None:
            self._login_credentials = LoginCredentials(_env_file=env_file_credentials)
        else:
            self._login_credentials = LoginCredentials()

        # Set connection configuration
        if env_file_connection is not None:
            self._connection_configuration = ConnectionConfiguration(_env_file=env_file_connection)
        else:
            self._connection_configuration = ConnectionConfiguration()

        # Session
        self._session = None

    def __enter__(self):
        """Open requests connection and login."""
        self._session = requests.Session()

        login_response = self._session.post(
            url=self._connection_configuration.login_url,
            data=self._login_credentials.json(),
            timeout=(
                self._connection_configuration.requests_connect,
                self._connection_configuration.requests_read,
            ),
        )

        if login_response.status_code != 200:
            if login_response.status_code in (400, 401):
                error_message = ReceivedError.parse_raw(login_response.text).error.errormessage
                self._session.close()
                raise XRTCException(
                    f"Login failed. {error_message}", self._connection_configuration.login_url
                )

            self._session.close()
            raise XRTCException(
                f"Login failed. Code: {login_response.status_code}",
                self._connection_configuration.login_url,
            )

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close requests connection."""
        self._session.close()

    def set_item(self, items: list[dict]):
        """Wrap for set item endpoint.

        Parameters:
            items (list[dict]): list of items to set, e.g. [{"portalid": "send", "payload": "sample"}]
        """
        # Parse request parameters
        request_parameters = SetItemRequest(items=items)

        # Make request
        set_item_response = self._session.post(
            url=self._connection_configuration.set_url,
            data=request_parameters.json(),
            timeout=(
                self._connection_configuration.requests_connect,
                self._connection_configuration.requests_read,
            ),
        )

        if set_item_response.status_code != 200:
            if set_item_response.status_code in (400, 401):
                error_message = ReceivedError.parse_raw(set_item_response.text).error.errormessage
                raise XRTCException(
                    f"Set item failed. {error_message}", self._connection_configuration.set_url
                )

            raise XRTCException(
                f"Set item failed. Code: {set_item_response.status_code}",
                self._connection_configuration.set_url,
            )

    def get_item(self, portals: list[dict] = None, polling: int = 0) -> ReceivedData:
        """Wrap get item endpoint.

        Parameters:
            portals (list[dict]): list of portals to get items from, e.g. [{"portalid": "send"}]
            polling (int): 0 - no polling, 1 - poll until there is new data, 2 - poll continuously

        Returns:
            ReceivedData: list of items, e.g. [{"portalid": "send", "payload": "sample", "servertimestamp": 123}]
        """
        # Parse request parameters
        request_parameters = GetItemRequest(portals=portals, polling=polling)

        # Make request
        get_item_response = self._session.post(
            url=self._connection_configuration.get_url,
            data=request_parameters.json(),
            timeout=(
                self._connection_configuration.requests_connect,
                self._connection_configuration.requests_read,
            ),
        )

        if get_item_response.status_code != 200:
            if get_item_response.status_code in (400, 401):
                error_message = ReceivedError.parse_raw(get_item_response.text).error.errormessage
                raise XRTCException(
                    f"Set item failed. {error_message}", self._connection_configuration.get_url
                )

            raise XRTCException(
                f"Set item failed. Code: {get_item_response.status_code}",
                self._connection_configuration.get_url,
            )

        return ReceivedData.parse_raw(get_item_response.text)
