"""
Middleware simplificado - Solo CORS y logging básico
(La autenticación ahora es por dependencias en endpoints)
"""

import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import structlog

logger = structlog.get_logger()


class SimpleLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware simple para logging de requests
    """
    
    def __init__(self, app):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log básico de requests"""
        
        start_time = time.time()
        
        # Log del request
        logger.info(
            "Request recibido",
            method=request.method,
            path=request.url.path,
            client_ip=self._get_client_ip(request)
        )
        
        # Procesar request
        response = await call_next(request)
        
        # Calcular tiempo de respuesta
        process_time = time.time() - start_time
        
        # Log de respuesta
        logger.info(
            "Request procesado",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time=f"{process_time:.3f}s"
        )
        
        # Agregar headers útiles
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-API-Version"] = "1.3.1"
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Obtener IP del cliente"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        if hasattr(request.client, "host"):
            return request.client.host
        
        return "unknown" 