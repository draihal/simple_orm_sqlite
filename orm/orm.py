"""
Tiny little ORM (Object Relational Mapper) for SQLite.
"""
import logging
import sqlite3
import os


logging.basicConfig(
    filename='simple_orm_sqlite.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO)


DATA_TYPES = {'str': 'TEXT', 'int': 'INTEGER', 'float': 'REAL'}
REQUIRED_OR_NOT = {'required': ' NOT NULL', 'not_required': ''}


def check_field_args(attr):
    if not isinstance(attr, tuple):
        raise Exception('Must be tuple with 2 args.')
    if len(attr) > 2:
        raise Exception('Only 2 args need. Data types and required or not, or \'foreign_key\' and table name.')
    if attr[0] not in DATA_TYPES and attr[0] != 'foreign_key':
        raise Exception('Unsupported format.')
    if attr[1] not in REQUIRED_OR_NOT and attr[0] != 'foreign_key':
        raise Exception('Wrong format, must be: \'required\' or \'not_required\'')


class Base:
    __tablename__ = ''
    __db__ = 'db.sqlite3'
    __path_to_db__ = os.path.join('' or os.getcwd(), __db__)

    def select_all(self):
        field_names = [k for k in self.__class__.__dict__.keys() if not k.startswith('__')]
        print('SELECT %s FROM %s;' % (', '.join(field_names), self.__class__.__tablename__))

    def create_table(self, cursor):
        table_name = self.__class__.__tablename__
        field_names = []
        fk = []
        for key_var in self.__dict__:
            attr = self.__dict__[key_var]
            check_field_args(attr)
            if attr[0] in DATA_TYPES:
                field_names.append(f'{key_var} {DATA_TYPES.get(attr[0])}{REQUIRED_OR_NOT.get(attr[1])}')
            elif attr[0] == 'foreign_key':
                field_names.append(f'{key_var} INTEGER NOT NULL')
                fk.append(f'FOREIGN KEY ({key_var}) REFERENCES {attr[1]}(id)')
                # project_id integer NOT NULL  https://www.sqlitetutorial.net/sqlite-python/create-tables/
        if field_names:
            column = f'id INTEGER PRIMARY KEY, {", ".join(field_names)}'
            sql = f'CREATE TABLE IF NOT EXISTS {table_name}({column}, {", ".join(fk)});' if fk else f'CREATE TABLE IF NOT EXISTS {table_name}({column});'
            print('sql', sql)
            logging.info(f'CREATE TABLE - {sql}')
            cursor.execute(sql)

    def save(self):
        with sqlite3.connect(Base.__path_to_db__) as connection:
            try:
                cursor = connection.cursor()
                logging.info("Create db connection")
                self.create_table(cursor)
            finally:
                logging.info("Connection close")
                cursor.close()

    def delete(self):
        # DROP TABLE [IF EXISTS] [schema_name.] table_name;

        # PRAGMA foreign_keys = OFF;
        # DROP TABLE addresses;
        # UPDATE people SET address_id = NULL;
        # PRAGMA foreign_keys = ON;
        pass
