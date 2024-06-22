
from fastapi import FastAPI, Request
from app.api.shots import router as shots_router
from app.api.cards import router as cards_router
from app.api.events import router as events_router
from app.api.products import router as products_router
from app.api.authentication import router as login_router
from app.api.file_upload import router as s3_upload_router
from app.api.search import router as search_router
from app.api.dashboard import router as dashboard_router
from app.api.llama_index import router as llama_index_router
from app.middlewares.middleware import AuthMiddleware
from app.core.sqllite import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
async def index():
    return {"message": "Success"}

app.add_middleware(AuthMiddleware)
app.include_router(shots_router)
app.include_router(cards_router)
app.include_router(events_router)
app.include_router(products_router)
app.include_router(login_router)
app.include_router(s3_upload_router)
app.include_router(search_router)
app.include_router(dashboard_router)
app.include_router(llama_index_router)
