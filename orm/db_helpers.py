#: Dictionary to map Python and SQLite data types
DATA_TYPES = {str: 'TEXT', int: 'INTEGER', float: 'REAL'}


def attrs(obj):
    return dict(i for i in vars(obj).items() if i[0][0] != '_')


def copy_attrs(obj, remove=None):
    if remove is None:
        remove = []
    return dict(i for i in attrs(obj).items() if i[0] not in remove)


def render_column_definitions(model):
    model_attrs = attrs(model).items()
    model_attrs = {k: v for k, v in model_attrs if k != 'db'}
    return ['%s %s' % (k, DATA_TYPES[v]) for k, v in model_attrs.items()]


def render_create_table_stmt(model):
    sql = 'CREATE TABLE {table_name} (id integer primary key autoincrement, {column_def});'
    column_definitions = ', '.join(render_column_definitions(model))
    params = {'table_name': model.__name__, 'column_def': column_definitions}
    return sql.format(**params)
