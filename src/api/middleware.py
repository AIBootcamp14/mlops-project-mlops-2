from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

from src.utils.logger import get_logger

logger = get_logger(__name__)

def register_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_method=["*"],
        allow_header=["*"]
    )

    @app.middleware("http")
    async def log_req_res(request: Request, call_next):
        logger.info(f"[Req] {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"[Res] {response.status_code}")
        return response
    
    
