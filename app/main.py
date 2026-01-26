from fastapi import FastAPI
from app.database import engine, Base
from app.routers.subject_router import router as subject_router
from app.routers.auth_router import router as auth_router
from app.core.logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(subject_router)
app.include_router(auth_router)

logger.info("FastAPI application initialized")
logger.info("Database tables created")
logger.info("Routers registered: subjects, auth")


@app.get("/")
async def read_root():
    logger.debug("Root endpoint accessed")
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application startup completed")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application shutdown")

