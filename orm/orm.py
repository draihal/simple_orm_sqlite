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

    def select_all(self):
        field_names = [k for k in self.__class__.__dict__.keys() if not k.startswith('__')]
        print('SELECT %s FROM %s;' % (', '.join(field_names), self.__class__.__tablename__))

    def create_table(self):
        with sqlite3.connect(Base.__db__) as connection:
            try:
                cursor = connection.cursor()
                table_name = self.__class__.__tablename__
                field_names = []
                fk = []
                print('self.__dict__', self.__dict__,)

                for key_var in self.__dict__:
                    print('key_var', key_var, 'attr', self.__dict__[key_var])
                    attr = self.__dict__[key_var]
                    if not isinstance(attr, tuple):
                        raise Exception('Must be tuple with args.')
                    if len(attr) > 2:
                        raise Exception('Only 2 args need. Data types and required or not, or \'foreign_key\' and table name.')
                    if attr[0] not in DATA_TYPES and attr[0] != 'foreign_key':
                        raise Exception('Unsupported format.')
                    if attr[1] not in REQUIRED_OR_NOT and attr[0] != 'foreign_key':
                        raise Exception('Wrong format, must be: \'required\' or \'not_required\'')
                    if attr[0] == 'foreign_key':
                        # attr[1]
                        pass
                    if attr[0] in DATA_TYPES:
                        field_names.append(f'{key_var} {DATA_TYPES.get(attr[0])}{REQUIRED_OR_NOT.get(attr[1])}')
                    elif attr[0] == 'foreign_key':
                        field_names.append(f'{key_var} INTEGER NOT NULL')
                        fk.append(f'FOREIGN KEY ({key_var}) REFERENCES {attr[1]}(id)')
                        # project_id integer NOT NULL  https://www.sqlitetutorial.net/sqlite-python/create-tables/
                print('field_names', field_names)
                if field_names:
                    column = f'id INTEGER PRIMARY KEY, {", ".join(field_names)}'
                    # column += ','.join(field_names)
                    fk = ', '.join(fk)
                    print('column', column, fk)
                    if fk:
                        sql = f'CREATE TABLE IF NOT EXISTS {table_name}({column}, {fk});'
                    else:
                        sql = f'CREATE TABLE IF NOT EXISTS {table_name}({column});'
                    print('sql', sql)
                    cursor.execute(sql)
            finally:
                cursor.close()

    def delete_table(self):
        pass
