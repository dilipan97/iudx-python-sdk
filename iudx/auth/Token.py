import json

from iudx.common.HTTPEntity import HTTPEntity
from iudx.common.HTTPResponse import HTTPResponse


class Token:
    """
    Provides token functionality for accessing
    single private resources
    """

    def __init__(
            self,
            auth_url: str = "https://authorization.iudx.org.in/auth/v1/token",
            body=None,
            headers=None):
        """
        Token class constructor for requesting tokens

        """
        if headers is None:
            headers = {"content-type": "application/json"}
        self.auth_url = auth_url
        self.body = body
        self.headers = headers
        self.credentials = None
        return

    def request_token(self) -> str:
        """
        Method to request a token for the added private resources

        Returns the credentials (access token, expiry, server) to access added the private resources
        """

        http_entity = HTTPEntity()
        response: HTTPResponse = http_entity.post(self.auth_url, json.dumps(self.body), self.headers)
        result_data = response.get_json()

        if response.get_status_code() == 200:
            self.credentials = result_data["results"]
            return self.credentials["accessToken"]
        else:
            raise RuntimeError(result_data["detail"])
