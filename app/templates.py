from db import db
from exceptions import TemplateException
from functools import wraps


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
    def delete_template(self, user_id: int, template_id: int) -> None:
        pass

    @classmethod
    @exception_handler
    def get_user_templates(cls, user_id: int):
        user_templates = db.fetch_by_param(
            table='template',
            columns=['id', 'name', 'body'],
            param='user_id',
            value=user_id
        )
        return user_templates
