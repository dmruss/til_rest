from fastapi import APIRouter

from .endpoints import users
from .endpoints import facts

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(facts.router, prefix="/facts", tags=["Facts"])