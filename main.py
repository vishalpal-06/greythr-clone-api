from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import get_images, admin, auth
from dbs.database import engine
from dbs import models

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8501",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_images.router)
app.include_router(admin.router)
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)