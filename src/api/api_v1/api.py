from fastapi import APIRouter

from .endpoints import facts

router = APIRouter()
router.include_router(facts.router, prefix="/facts", tags=["Facts"])