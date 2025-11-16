from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app import todo,auth

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def welcome_page():
    return {"messge":"Welcom to your's todo's for achieviement..."}

app.include_router(todo.router)
app.include_router(auth.router)