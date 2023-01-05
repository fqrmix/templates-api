import sqlite3
from typing import List, Tuple
from functools import wraps
from exceptions import DatabaseException

class Database:
    """ Класс для работы с БД """
    def exception_handler(method):
        @wraps(method)
        def _wrapper(*method_args, **method_kwargs):
            try:
                return method(*method_args, **method_kwargs)
            except Exception as e:
                raise DatabaseException(e)
        return _wrapper

    @exception_handler
    def __init__(self, path: str) -> None:
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    @exception_handler
    def insert(self, table: str, column_values: dict) -> None:
        columns = ', '.join(column_values.keys())
        values = [tuple(column_values.values())]
        placeholders = ', '.join("?" * len(column_values.keys()))
        self.cursor.executemany(
            f"INSERT into {table} "
            f"({columns}) "
            f"VALUES ({placeholders})",
            values
        )
        self.connection.commit()

    @exception_handler
    def fetch_all(self, table: str, columns: List[str]) -> List[Tuple]:
        columns_joined = ", ".join(columns)
        self.cursor.execute(f"SELECT {columns_joined} FROM {table}")
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result
    
    @exception_handler
    def fetch_by_param(self, table: str, columns: List[str], param: str, value: str) -> List[Tuple]:
        columns_joined = ", ".join(columns)
        self.cursor.execute(f"SELECT {columns_joined} FROM {table} where {param}={value}")
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result

    @exception_handler
    def delete(self, table: str, row_id: int) -> None:
        row_id = int(row_id)
        self.cursor.execute(f"DELETE FROM {table} where id={row_id}")
        self.connection.commit()
