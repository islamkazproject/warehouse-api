import uvicorn
from fastapi import FastAPI
from api import router as api_router
from core.config import settings

app = FastAPI(
    title=settings.project_name
)
app.include_router(
    api_router,
    prefix=settings.api.prefix,
)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )