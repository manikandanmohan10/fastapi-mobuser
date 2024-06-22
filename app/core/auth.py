from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.jwt_auth import JWTManager


jwt_manager = JWTManager()
security = HTTPBearer()

roles_permissions = {
    "reviewer": ["review"],
    "editor": ["edit", "create", "review"],
    "admin": ["edit", "create", "review", "delete"]
}

def check_permissions(user_role: str, required_permission: str) -> bool:
    return required_permission in roles_permissions.get(user_role, [])

async def authorize_user(request: Request, required_permission: str):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_role = user.get("role")
    if not user_role:
        raise HTTPException(status_code=403, detail="Role not found")

    if required_permission and not check_permissions(user_role, required_permission):
        raise HTTPException(status_code=403, detail="Permission denied")

    return user

# Dependency wrapper
def get_current_user(required_permission: str):
    async def dependency(request: Request):
        return await authorize_user(request, required_permission)
    return dependency
