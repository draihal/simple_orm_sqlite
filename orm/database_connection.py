import logging
import sqlite3

from .orm import Model


class Database:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._connection = None
        self.connected = False
        self.Model = type('Model%s' % str(self), (Model,), {'db': self})

    @property
    def connection(self):
        logging.info(f'DB connection to {self.args}')
        if self.connected:
            return self._connection
        self._connection = sqlite3.connect(*self.args, **self.kwargs)
        self._connection.row_factory = sqlite3.Row
        self.connected = True
        return self._connection

    def close(self):
        if self.connected:
            self.connection.close()
        logging.info(f'DB connection close')
        self.connected = False

    def commit(self):
        logging.info(f'DB commit')
        self.connection.commit()

    def execute(self, sql, *args):
        logging.info(f'DB execute: {sql}, {args}')
        return self.connection.execute(sql, args)

    def executescript(self, script):
        logging.info(f'DB executescript: {script}')
        self.connection.cursor().executescript(script)
        self.commit()
