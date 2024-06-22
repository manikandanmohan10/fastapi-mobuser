import time
from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.jwt_auth import JWTManager
from fastapi.exceptions import ResponseValidationError


jwt_manager = JWTManager()


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            start_time = time.time()
            # if request.url.path != '/login':
                # Extract the access token from the Authorization header
                # authorization: str = request.headers.get('Authorization')
                # if not authorization or not authorization.startswith("Bearer "):
                #     return Response("Access token not found", status_code=401)
                
                # token = authorization.split(" ")[1]
                # user = jwt_manager.decode_token(token)  # Decode the JWT token
                # if not user:
                #     return Response("Authentication failed", status_code=401)
                
                # Attach user information to the request state
                # request.state.user = user
            request.state.user = {'user': 'user.username'}

            response = await call_next(request)

            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)
