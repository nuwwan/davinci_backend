from fastapi import FastAPI
from app.routers import subject
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(subject.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}