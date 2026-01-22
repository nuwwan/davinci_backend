from fastapi import FastAPI
from backend.app.routers import subjectRouter
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(subjectRouter.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}