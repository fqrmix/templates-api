from db import db
from functools import wraps
from pydantic import BaseModel
from typing import Union

class User(BaseModel):
    id: Union[int, None]
    name: Union[str, None]

class UserController:
    """ Класс для работы с пользователями """
    def exception_handler(method):
        @wraps(method)
        def _wrapper(*method_args, **method_kwargs):
            try:
                return method(*method_args, **method_kwargs)
            except Exception as e:
                raise Exception(e)
        return _wrapper

    @classmethod
    @exception_handler
    def get_users(cls):
        return db.fetch_all(
            table='user',
            columns=['id', 'name']
        )

    @classmethod
    @exception_handler
    def get_user_info(cls, id: int) -> Union[User, None]:
        user = db.fetch_by_param(
            table='user',
            columns=['id', 'name'],
            param='id',
            value=id
        )
        if user == []:
            return None

        return User(
            id=user[0]['id'],
            name=user[0]['name']
        )

    @classmethod
    @exception_handler
    def add_user(cls, name: str, id: int) -> None:
        column_values = {
                'id': int(id),
                'name': name
            }
        db.insert(
            table='user',
            column_values=column_values
        )

    @classmethod    
    @exception_handler
    def delete_user(cls, id: int) -> None:
        db.delete(
            table='user',
            row_id=id
        )
