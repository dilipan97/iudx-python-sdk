import json

from iudx.common.HTTPEntity import HTTPEntity
from iudx.common.HTTPResponse import HTTPResponse


class Token:
    """
    Provides token functionality for accessing
    the private resources
    """

    def __init__(
            self,
            auth_url: str = "https://authorization.iudx.org.in/auth/v1/token",
            refresh_token: str = None,
            client_id: str = None,
            client_secret: str = None,
            headers: dict = None):
        """
        Token class constructor for requesting tokens

        Args:
            auth_url (String): Authorization server url.
            refresh_token (String): Keycloak Issued token.
            client_id (String): Keycloak Issued clientId.
            client_secret (String): Keycloak Issued clientSecret.
            headers (Dict): Headers passed with the API Request.
        """
        if headers is None:
            headers = {"content-type": "application/json"}

        if refresh_token is not None:
            headers.update({"Authorization": refresh_token})
        elif client_id is not None and client_secret is not None:
            headers.update({"clientId": client_id, "clientSecret": client_secret})
        else:
            raise RuntimeError("Token or clientId/clientSecret missing")

        self.auth_url = auth_url
        self.headers = headers
        self.credentials = None
        return

    def request_token(
            self,
            item_id: str,
            item_type: str,
            role: str) -> str:
        """
        Method to request a token for the private resources

        Args:
            item_id (String): Id of the Resource.
            item_type (String): Type of the Resource.
            role (String): Role of the User.

        Returns:
             access_token (String): Token to access the private resources
        """
        body = {"itemId": item_id, "itemType": item_type, "role": role}

        http_entity = HTTPEntity()
        response: HTTPResponse = http_entity.post(self.auth_url, json.dumps(body), self.headers)
        result_data = response.get_json()

        if response.get_status_code() == 200:
            self.credentials = result_data["results"]
            access_token = self.credentials["accessToken"]
            return access_token
        else:
            raise RuntimeError(result_data["detail"])
