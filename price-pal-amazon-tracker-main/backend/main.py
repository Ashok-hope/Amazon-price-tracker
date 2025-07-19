
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from contextlib import asynccontextmanager
import logging

from auth import get_current_user
from models import User
from price_checker import PriceChecker
from scheduler import start_scheduler
import crud

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    pass


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Amazon Price Tracker API",
    description="Track Amazon product prices and get notified when prices drop",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log all requests for debugging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error(f"Unhandled error: {exc}", exc_info=True)
        raise
    logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
    return response

# Include routers
from auth import router as auth_router
from crud import router as crud_router
from price_checker import router as price_router

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(crud_router, prefix="/api", tags=["products"])
app.include_router(price_router, prefix="/price", tags=["price-checking"])


@app.get("/")
async def root():
    logger.info("Root endpoint hit.")
    return {"message": "Amazon Price Tracker API is running!"}


@app.get("/health")
async def health_check():
    logger.info("Health check endpoint hit.")
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
