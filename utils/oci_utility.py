import base64

class OCIUtility:
    @staticmethod
    def get_authorization_token(client_id: str, client_secret: str) -> str:
        """Generate an Authorization Token for OCI API requests."""
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return f"Basic {encoded_credentials}"