"""
Tiny little ORM (Object Relational Mapper) for SQLite.
"""
import logging
import sqlite3


logging.basicConfig(
    filename='simple_orm_sqlite.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO)


DATA_TYPES = {'str': 'TEXT', 'int': 'INTEGER', 'float': 'REAL'}
REQUIRED_OR_NOT = {'required': ' NOT NULL', 'not_required': ''}


class Base:
    __tablename__ = ''
    __db__ = 'db.sqlite3'

    # def __init__(self, ):
    #     self.table_name = self.__tablename__
    #     self.db = db
    #     self.field_names = {fild for fild in self.__class__.__dict__.keys()
    #                         if not fild.startswith('__')}

    def select_all(self):
        field_names = [k for k in self.__class__.__dict__.keys() if not k.startswith('__')]
        print('SELECT %s FROM %s;' % (', '.join(field_names), self.__class__.__tablename__))

    def create(self):
        with sqlite3.connect(Base.__db__) as connection:
            try:
                cursor = connection.cursor()
                table_name = self.__class__.__tablename__
                field_names = []

                for key_var in self.__dict__:
                    attr = self.__dict__[key_var]
                    if not isinstance(attr, tuple):
                        raise Exception('Must be tuple with args.')
                    if len(attr) > 2:
                        raise Exception('khb,jhb,jhb,jhb,jhb,!')
                    if attr[0] not in DATA_TYPES:
                        raise Exception('Unsupported format.')
                    if attr[1] not in REQUIRED_OR_NOT:
                        raise Exception('Wrong format, must be: \'required\' or \'not_required\'')

                    field_names.append(f'{key_var} {DATA_TYPES.get(attr[0])}{REQUIRED_OR_NOT.get(attr[1])}')
                if field_names:
                    column = ' id INTEGER PRIMARY KEY, '
                    column += ','.join(field_names)
                    sql = 'CREATE TABLE IF NOT EXISTS {table_name}({column});'.format(table_name=table_name, column=column)
                    cursor.execute(sql)
            finally:
                cursor.close()
