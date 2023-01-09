from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from users import UserController, User
from templates import TemplateController, Template

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
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}

###############
# Users block #
###############

@app.get("/users")
def read_users():
    return UserController.get_users()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    try:
        return UserController.get_user_info(user_id)
    except Exception as e:
        return {
            'http_code': 500,
            'error': e
        }

@app.post("/users/add")
def add_user(user: User):
    try:
        UserController.add_user(
            name=user.name, 
            telegram_id=user.telegram_id, 
            id=user.id)
        return 200
    except Exception as e:
        return {
            'http_code': 500,
            'error': e
        }

###################
# Templates block #
###################

@app.get("/templates/{user_id}")
def read_templates(user_id: int):
    return TemplateController.get_user_templates(user_id)

@app.post("/templates/add")
def add_template(template: Template):
    try:
        TemplateController.add_template(template.user_id, template.name, template.body)
        return template
    except Exception as e:
        return {
            'http_code': 500,
            'error': e
        }

@app.post("/templates/delete/{template_id}")
def read_templates(template_id: int):
    return TemplateController.delete_template(template_id)
