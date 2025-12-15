from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import logging
import asyncio

# --- Core imports ---
from app.core.config import get_settings
from app.api.routes import models, generate, health
from app.services.redis import RedisService
from app.workers.manager import start_worker_manager, stop_worker_manager
from app.models.schema import ErrorResponse

# --- Custom middleware imports ---
from app.middleware.rate_limiter import RateLimitMiddleware
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.cache import CacheMiddleware

# --- Connection pool import ---
from app.core.connection_pool import get_http_client, close_http_client
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Lifespan context manager for startup/shutdown

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting application...")
    redis_service = RedisService()
    await redis_service.connect()
    app.state.redis = redis_service
    logger.info("Redis connected successfully")

    # Initialize global HTTP connection pool
    http_client = get_http_client()
    app.state.http_client = http_client
    logger.info("HTTP connection pool initialized")

    # Start worker manager in background
    asyncio.create_task(start_worker_manager())
    logger.info("Worker manager started")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    await stop_worker_manager()
    await redis_service.disconnect()
    await close_http_client()
    logger.info("Application shutdown complete")

# Create FastAPI app

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade API Gateway for Fal.ai models with queue management",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# --- Middleware registration order ---
# 1. Logging (first, logs all requests)
app.add_middleware(RequestLoggingMiddleware)
# 2. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 3. Cache (for GET endpoints)
app.add_middleware(CacheMiddleware, cacheable_paths=[
    f"{settings.API_V1_PREFIX}/models",
    f"{settings.API_V1_PREFIX}/models/categories",
    f"{settings.API_V1_PREFIX}/models/search",
    f"{settings.API_V1_PREFIX}/models/",
    f"{settings.API_V1_PREFIX}/health",
])
# 4. Rate Limiting (after CORS, after cache)
app.add_middleware(RateLimitMiddleware)



# Request timing middleware (robust to error responses)
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        process_time = time.time() - start_time
        # If exception, try to add header to a new response
        resp = JSONResponse(
            status_code=500,
            content={"error": "InternalServerError", "message": str(exc)}
        )
        resp.headers["X-Process-Time"] = str(process_time)
        return resp
    process_time = time.time() - start_time
    # Only add header if not already started
    if not response.headers.get("X-Process-Time"):
        response.headers["X-Process-Time"] = str(process_time)
    return response

# Request validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="ValidationError",
            message="Invalid request data",
            details={"errors": exc.errors()}
        ).model_dump()
    )


# HTTP 429 handler (rate limit exceeded)
@app.exception_handler(429)
async def http_429_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=429,
        content=ErrorResponse(
            error="RateLimitExceeded",
            message=exc.detail or "Rate limit exceeded. Please try again later.",
            details=None
        ).model_dump()
    )

# HTTP exception handler (all others)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.detail,
            details=None
        ).model_dump()
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message=str(exc) if settings.DEBUG else "An internal error occurred",
            details={"type": exc.__class__.__name__} if settings.DEBUG else None
        ).model_dump()
    )

# Include routers
app.include_router(health.router, prefix=settings.API_V1_PREFIX, tags=["Health"])
app.include_router(models.router, prefix=settings.API_V1_PREFIX, tags=["Models"])
app.include_router(generate.router, prefix=settings.API_V1_PREFIX, tags=["Generation"])

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "operational"
    }
