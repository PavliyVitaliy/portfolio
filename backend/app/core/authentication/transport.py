from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(
    # TODO update
    tokenUrl="auth/jwt/login"
)
