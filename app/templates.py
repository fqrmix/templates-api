from db import db
from exceptions import TemplateException
from functools import wraps
from pydantic import BaseModel
from typing import Union, List

class Template(BaseModel):
    id: Union[int, None]
    name: str
    body: str
    user_id: Union[int, None]

class TemplateController:
    """ Класс для работы с шаблонами """

    def exception_handler(method):
        @wraps(method)
        def _wrapper(*method_args, **method_kwargs):
            try:
                return method(*method_args, **method_kwargs)
            except Exception as e:
                raise TemplateException(e)
        return _wrapper

    @classmethod
    @exception_handler
    def add_template(cls, user_id: int, name: str, body: str) -> None:
        db.insert(
            table='template',
            column_values={
                'name': name,
                'body': body,
                'user_id': user_id
            }
        )

    @classmethod
    @exception_handler
    def delete_template(cls, template_id: int) -> None:
        db.delete(
            table='template',
            row_id=template_id
        )


    @classmethod
    @exception_handler
    def get_user_templates(cls, user_id: int):
        user_templates = db.fetch_by_param(
            table='template',
            columns=['id', 'name', 'body', 'user_id'],
            param='user_id',
            value=user_id
        )

        if user_templates is None:
            return None
        
        result = []
        for template in user_templates:
            result.append(Template(
                id=template['id'],
                name=template['name'],
                body=template['body'],
                user_id=template['user_id']
            ))
        return result
