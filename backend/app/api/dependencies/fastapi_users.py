import uuid

from fastapi_users import FastAPIUsers

from core.models import User
from .user_manager import get_user_manager
from .backend import authentication_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [authentication_backend],
)
