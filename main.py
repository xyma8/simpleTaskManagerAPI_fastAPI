from fastapi import FastAPI, WebSocket

from app.api.endpoints import tasks, users
from app.core.logging_config import setup_logger
from app.core.websocket import websocket_endpoint

logger = setup_logger()

app = FastAPI()

# Register the routers with respective prefixes
app.include_router(users.router, prefix="/auth")
app.include_router(tasks.router)


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    """WebSocket route that handles WebSocket connections."""
    await websocket_endpoint(websocket)
    logger.info("WebSocket connection established")


@app.middleware("http")
async def log_requests(request, call_next):
    """Middleware to log HTTP requests and responses."""
    logger.info(f"Request path: {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    """Global exception handler that logs exceptions."""
    logger.error(f"Unhandled exception at {request.url.path}: {exc}")
    return {"message": "An error occurred", "details": str(exc)}
