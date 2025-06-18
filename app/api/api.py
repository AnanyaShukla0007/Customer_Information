from fastapi import APIRouter
from app.api.endpoints import customers, employments, registration

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    customers.router,
    prefix="/customers",
    tags=["customers"]
)

api_router.include_router(
    employments.router,
    prefix="/employments",
    tags=["employments"]
)

api_router.include_router(
    registration.router,
    prefix="/registration",
    tags=["registration"]
) 