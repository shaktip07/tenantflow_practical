import jwt
from typing import Any
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.base.response import jwt_response_error
import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

NO_AUTH_URLS = [
    "/login",
    "/tenantflow/docs",
    "/tenantflow/admin/",
    "/tenantflow/redoc",
    "/docs",
    "/openapi.json",
    "/tenantflow/openapi.json",
    "/api/admin/login",
    "/api/admin/register",
    "/tenantflow/login",
]


class JWTAuthMiddleware(BaseHTTPMiddleware):
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    async def dispatch(self, request: Request, call_next):
        request.state.api_key = None
        print(f"request.url.path : {request.url.path}")
        if request.url.path in NO_AUTH_URLS or "tenantflow" in request.url.path:
            return await call_next(request)

        token = await self.get_token(request)
        if not token:
            return jwt_response_error("Invalid or missing token")

        if isinstance(token, bool) and token == True:
            return await call_next(request)

        try:
            user_info = self.decode_token(token)
            print(user_info, "user_info")
            request.state.user = user_info
            request.state.org = str(user_info.get("organization_id"))
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            return jwt_response_error(f"Invalid token: {str(e)}")

        return await call_next(request)

    async def get_token(self, request: Request) -> Any:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jwt_response_error("Invalid or missing Authorization header")

        if "JWT" in auth_header:
            return auth_header.split()[1]

        return False

    def decode_token(self, token: str) -> dict:
        try:
            result = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return result
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            raise e
