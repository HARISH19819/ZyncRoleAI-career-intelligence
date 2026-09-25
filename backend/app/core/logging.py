import logging
import sys
import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("zyncrole")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        # Add request_id to state
        request.state.request_id = request_id
        
        # Log incoming request (without sensitive bodies or headers)
        logger.info(f"[{request_id}] -> {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            logger.info(f"[{request_id}] <- {request.method} {request.url.path} {response.status_code} ({duration_ms}ms)")
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as exc:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(f"[{request_id}] ERROR {request.method} {request.url.path}: {exc} ({duration_ms}ms)")
            raise
