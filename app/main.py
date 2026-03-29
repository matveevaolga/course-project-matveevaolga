from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from app.core.errors import AppError
from app.features.routes import router as features_router

app = FastAPI(title="Feature Vote App", version="0.1.0")

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware для security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    # Базовые security headers для API
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Strict-Transport-Security для продакшена
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

    return response


app.include_router(features_router)


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
def health_check():
    return {"status": "ok"}


_db = {"items": []}


@app.post("/items")
def create_item(name: str):
    if not name or len(name) > 100:
        raise AppError(
            code="validation_error", msg="name must be 1..100 chars", status=422
        )
    item = {"id": len(_db["items"]) + 1, "name": name}
    _db["items"].append(item)
    return item


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for it in _db["items"]:
        if it["id"] == item_id:
            return it
    raise AppError(code="not_found", msg="item not found", status=404)
