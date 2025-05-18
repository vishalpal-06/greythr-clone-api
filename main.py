from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import get_images

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8501",
    "http://localhost:8080",
    "http://localhost:5173"
    # Add other origins as needed
]

# Allow frontend (React) to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


app.include_router(get_images.router)