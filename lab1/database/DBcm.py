from pymysql import connect
from pymysql.err import OperationalError

# В класс наследуем три баззовых метода с ними порядок передачи управления
# with DBContextManger (...) as curdor:  использование конструкции с именем класса
# приводит к передачи управление init -> enter -> в начало класса(методы init)

# Конструкция with работает совместно с классом DBContextManger,
# при выполнении оператора with передается управление init,
# после его инициализации методу enter он может закончиться двумя вариантоми: или вернеться курсор или ничего,
# если  вернулось ничего, значит произошла ошибка подключения. Делаем фиктивную ошибку
# Если все успешно управление все равно передаеться exit
class DBContextManager:
    def __init__(self, db_connect: dict):
        self.conn = None
        self.cursor = None
        self.db_connect = db_connect

    def __enter__(self):
        try:
            self.conn = connect(**self.db_connect)  # Переменная подключения
            self.cursor = self.conn.cursor()        # Объект курсор при подключении
            self.conn.begin()                       # Начинаем транзакцию
            return self.cursor
        except OperationalError as err:
            print(err.args)                         # Тут пишет не удалось подключиться
            return None                             # Возвращает в случае НЕ успешного подключения

    def __exit__(self, exc_type, exc_val, exc_tb):  # Не обходиться никогда или ошибка или чистка
        if exc_type:
            print(exc_type)
            print(exc_val)
        if self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        return True
