from .db_helpers import attrs, copy_attrs, render_create_table_stmt


class Manager:

    def __init__(self, db, model, type_check=True):
        self.db = db
        self.model = model
        self.table_name = model.__name__
        self.type_check = type_check
        if not self._hastable():
            self.db.executescript(render_create_table_stmt(self.model))

    def all(self):
        result = self.db.execute(f'SELECT * FROM {self.table_name}')
        return (self.create(**row) for row in result.fetchall())

    def create(self, **kwargs):
        obj = object.__new__(self.model)
        obj.__dict__ = kwargs
        return obj

    def delete(self, obj):
        sql = 'DELETE from %s WHERE id = ?'
        self.db.execute(sql % self.table_name, obj.id)

    def get(self, id):
        sql = f'SELECT * FROM {self.table_name} WHERE id = ?'
        result = self.db.execute(sql, id)
        row = result.fetchone()
        if not row:
            msg = 'Object%s with id does not exist: %s' % (self.model, id)
            raise ValueError(msg)
        return self.create(**row)

    def has(self, id):
        sql = f'SELECT id FROM {self.table_name} WHERE id = ?'
        result = self.db.execute(sql, id)
        return True if result.fetchall() else False

    def save(self, obj):
        if 'id' in obj.__dict__ and self.has(obj.id):
            msg = 'Object%s id already registred: %s' % (self.model, obj.id)
            raise ValueError(msg)
        clone = copy_attrs(obj, remove=['id'])
        self.type_check and self._isvalid(clone)
        column_names = '%s' % ', '.join(clone.keys())
        column_references = '%s' % ', '.join('?' for i in range(len(clone)))
        sql = 'INSERT INTO %s (%s) VALUES (%s)'
        sql = sql % (self.table_name, column_names, column_references)
        result = self.db.execute(sql, *clone.values())
        obj.id = result.lastrowid
        return obj

    def update(self, obj):
        clone = copy_attrs(obj, remove=['id'])
        self.type_check and self._isvalid(clone)
        where_expressions = '= ?, '.join(clone.keys()) + '= ?'
        sql = 'UPDATE %s SET %s WHERE id = ?' % (self.table_name, where_expressions)
        self.db.execute(sql, *(list(clone.values()) + [obj.id]))

    def _hastable(self):
        sql = 'SELECT name len FROM sqlite_master WHERE type = ? AND name = ?'
        result = self.db.execute(sql, 'table', self.table_name)
        return True if result.fetchall() else False

    def _isvalid(self, attr_values):
        attr_types = attrs(self.model)
        value_types = {a: v.__class__ for a, v in attr_values.items()}

        for attr, value_type in value_types.items():
            if value_type is not attr_types[attr]:
                msg = "%s value should be type %s not %s"
                raise TypeError(msg % (attr, attr_types[attr], value_type))
