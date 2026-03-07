"""
Módulo de middlewares FastAPI
"""

from .auth import SimpleLoggingMiddleware

# Placeholder para middlewares futuros
# from .error_handler import ErrorHandlerMiddleware
# from .cors import CORSMiddleware

__all__ = [
    "SimpleLoggingMiddleware"
    # "ErrorHandlerMiddleware",
    # "CORSMiddleware"
] 