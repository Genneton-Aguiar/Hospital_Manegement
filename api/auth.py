from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from keycloak import KeycloakOpenID
from django.conf import settings

KEYCLOAK_VERIFY_SSL = settings.KEYCLOAK_VERIFY_SSL
KEYCLOAK_SERVER_URL = settings.KEYCLOAK_SERVER_URL
KEYCLOAK_REALM = settings.KEYCLOAK_REALM
KEYCLOAK_CLIENT_ID = settings.KEYCLOAK_CLIENT_ID
KEYCLOAK_CLIENT_SECRET  = settings.KEYCLOAK_CLIENT_SECRET


class KeycloakAuthentication(BaseAuthentication):
    def __init__(self):
        self.keycloak_openid = KeycloakOpenID(
            server_url= KEYCLOAK_SERVER_URL,
            client_id= KEYCLOAK_CLIENT_ID,
            realm_name= KEYCLOAK_REALM,
            client_secret_key= KEYCLOAK_CLIENT_SECRET,
            verify= KEYCLOAK_VERIFY_SSL,
        )

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            user_info = self.keycloak_openid.userinfo(token)
            if not user_info:
                raise AuthenticationFailed("Token inválido ou expirado.")
            return (user_info, token)
        except Exception:
            raise AuthenticationFailed("Erro ao autenticar com Keycloak.")
        