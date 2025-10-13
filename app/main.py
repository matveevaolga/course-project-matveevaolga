from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.errors import AppError
from app.core.metrics import track_performance
from app.features.routes import router as features_router

app = FastAPI(title="SecDev Course App", version="0.1.0")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(features_router)

_db = {"items": []}


@app.exception_handler(AppError)
async def handle_app_error(req: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.msg}},
    )


@app.exception_handler(HTTPException)
async def handle_http_error(req: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else "http_error"
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "http_error", "message": detail}},
    )


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
@track_performance("GET /health")
def health_check():
    return {"status": "ok"}


@app.post("/items")
@track_performance("POST /items")
def create_item(name: str):
    if not name or len(name) > 100:
        raise AppError(
            code="validation_error", msg="name must be 1..100 chars", status=422
        )
    item = {"id": len(_db["items"]) + 1, "name": name}
    _db["items"].append(item)
    return item


@app.get("/items/{item_id}")
@track_performance("GET /items/{id}")
def get_item(item_id: int):
    for it in _db["items"]:
        if it["id"] == item_id:
            return it
    raise AppError(code="not_found", msg="item not found", status=404)
