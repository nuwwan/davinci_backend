from fastapi import FastAPI
from app.database import engine, Base
from app.routers.subject_router import router as subject_router
from app.routers.auth_router import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(subject_router)
app.include_router(auth_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
