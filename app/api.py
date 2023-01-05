from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users import UserController
from typing import Union
from pydantic import BaseModel
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

class User(BaseModel):
    id: Union[int, None]
    name: Union[int, None]
    telegram_id: Union[int, None]

@app.get("/users")
def read_users():
    return UserController.get_users()

@app.post("/users/delete/{user_id}")
def delete_user(user: User):
    try:
        UserController.delete_user(user.id)
        return 200
    except Exception as e:
        return [e, 500]

@app.post("/users/add")
def add_user(user: User):
    try:
        UserController.add_user(
            name=user.name, 
            telegram_id=user.telegram_id, 
            id=user.id)
        return 200
    except Exception as e:
        return [e, 500]

###################
# Templates block #
###################

class Template(BaseModel):
    name: str
    body: str
    user_id: int

@app.get("/templates/{user_id}")
def read_templates(user_id: int):
    return TemplateController.get_user_templates(user_id)

@app.post("/templates/add")
def add_template(template: Template):
    try:
        TemplateController.add_template(template.user_id, template.name, template.body)
        return template
    except Exception as e:
        return [e, 500]
