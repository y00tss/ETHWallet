from fastapi import APIRouter, Depends

from models.user import User

from services.utils.base_config import (
    auth_backend,
    fastapi_users,
)
from schemas.user import (
    UserRead,
    UserCreate,
)
from database.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

current_user = fastapi_users.current_user()


@router.get("/users/me", status_code=200, response_model=UserRead)
async def get_user(
        user: User = Depends(current_user),
        db: AsyncSession = Depends(get_async_session),
):
    """
    Get a specific user by id.
    """
    return user
