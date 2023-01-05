from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, List, Tuple
from users import UserController
from templates import TemplateController

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

###############
# Users block #
###############

@app.get("/users")
def read_users():
    return UserController.get_users()

@app.post("/users/delete/{user_id}")
def delete_user(user_id: int):
    try:
        UserController.delete_user(user_id)
        return 200
    except Exception as e:
        return [e, 500]

@app.post("/users/add")
def add_user(name: str, telegram_id: int, id = None):
    try:
        UserController.add_user(name, telegram_id, id)
        return 200
    except Exception as e:
        return [e, 500]

###################
# Templates block #
###################

@app.get("/templates/{user_id}")
def read_templates(user_id: int):
    return TemplateController.get_user_templates(user_id)

@app.post("/templates/add")
def add_template(name: str, body: str, user_id: int):
    try:
        TemplateController.add_template(user_id, name, body)
        return 200
    except Exception as e:
        return [e, 500]
