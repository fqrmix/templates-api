from db import db
from functools import wraps

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
            columns=['id', 'name', 'telegram_id']
        )

    @classmethod
    @exception_handler
    def add_user(cls, name: str, telegram_id: int, id = None) -> None:
        column_values = \
            {
                'name': name,
                'telegram_id': telegram_id
            }\
            if id is None else\
            {
                'id': int(id),
                'name': name,
                'telegram_id': telegram_id
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
