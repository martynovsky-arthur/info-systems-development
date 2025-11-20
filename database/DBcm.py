from pymysql import connect
from pymysql.cursors import DictCursor
from pymysql.err import OperationalError


class DBContextManager:
    def __init__(self, db_connect: dict):
        self.db_connect = db_connect
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = connect(**self.db_connect, autocommit=False, cursorclass=DictCursor)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            raise RuntimeError(f'DB connection error: {err}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        return False  # не подавляем исключения
