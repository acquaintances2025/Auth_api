from .test.healthz import test_router
from .auth.router import auth_router
from .profile.router import profile_router

__all__ = [
    "test_router",
    "auth_router",
    "profile_router"
]