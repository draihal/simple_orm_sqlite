"""
Tiny little ORM (Object Relational Mapper) for SQLite.
"""
import logging

from .db_helpers import attrs
from .manager import Manager

logging.basicConfig(
    filename='simple_orm_sqlite.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO)


class Model:
    db = None

    def delete(self, type_check=True):
        return self.__class__.manager(type_check=type_check).delete(self)

    def save(self, type_check=True):
        return self.__class__.manager(type_check=type_check).save(self)

    def update(self, type_check=True):
        return self.__class__.manager(type_check=type_check).update(self)

    @property
    def public(self):
        return attrs(self)

    def __repr__(self):
        return str(self.public)

    @classmethod
    def manager(cls, db=None, type_check=True):
        return Manager(db if db else cls.db, cls, type_check)

