from fastapi import FastAPI, status
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

description = "API based on FastAPI"

app = FastAPI(title="Simple Social app API", description=description)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# disable sqlalchemy table creation
# models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello, Sailor"}


@app.get("/author", status_code=status.HTTP_200_OK)
def author_info():
    return {"name": "Vleforn"}
