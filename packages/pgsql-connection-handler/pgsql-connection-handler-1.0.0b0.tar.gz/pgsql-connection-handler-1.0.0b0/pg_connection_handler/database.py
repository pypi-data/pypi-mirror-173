import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import NamedTupleCursor

from pg_connection_handler.exceptions import (
    ConnectionDoesNotExist,
    ImproperlyConfigured,
)


DEFAULT_DB_ALIAS = 'default'




class DatabaseHandler:
    """
    Stores all the initialized ``Database`` objects. The ``Database`` objects
    may have an open database connection or the connection might be closed.
    """

    def __init__(self):
        self._databases = {}


    def get(self, db_alias=DEFAULT_DB_ALIAS, reconnect_if_closed=True):
        """
        Return the database object related to a ``db_alias``. If a db alias
        is not provided: use the ``DEFAULT_DB_ALIAS`` instead (which is
        "default").

        If the database connection is closed: reconnect.

        If the database is not found, this raises ``ConnectionDoesNotExist``.

        :param db_alias:
        :param reconnect_if_closed:
        """
        db = self._databases.get(db_alias, None)
        if not db:
            raise ConnectionDoesNotExist(db_alias)
        if db.conn.closed and reconnect_if_closed:
            db.connect()
        return db


    def get_connection(self, db_alias=DEFAULT_DB_ALIAS, reconnect_if_closed=True):
        """
        A shortcut method to return the database connection directly instead
        of first getting the database via ``get``.
        """
        db = self.get(db_alias, reconnect_if_closed)
        return db.conn


    def register(self, db):
        """
        Register the database object to the registry so that it may be
        retrieved later.
        """
        if not self._databases.get(db.alias, None):
            self._databases[db.alias] = db


    def close(self, db_alias=DEFAULT_DB_ALIAS):
        """
        Close the database connection for the database related to the alias.
        """
        db = self.get(db_alias)
        if not db.conn.closed:
            db.conn.close()


    def close_all(self):
        """
        Close all database connections for the databases in the registry.
        """
        for db_alias, db in self._databases.items():
            if not db.conn.closed:
                db.conn.close()


    def reset(self):
        """
        Close all database connections and reset the registry.
        """
        self.close_all()
        self._databases = {}



databases = DatabaseHandler()




class Database:
    """
    An object representing a PostgreSQL database.

    The ``connection_dict`` argument's value should be in the following
    format:

    .. code-block:: python

        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        from psycopg2.extras import NamedTupleCursor

        DATABASES = {
            'my_database_alias': {
                'dbname': 'mydatabase',
                'user': 'guido',
                'password': 'SuperS3cr!t',
                'host': 'localhost',
                'port': '5432',
                'sslmode': 'disable',
                'application_name': 'myapp',

                # These are the default values for "options":
                'options': {
                    'isolation_level': ISOLATION_LEVEL_AUTOCOMMIT,
                    'default_cursor_factory': NamedTupleCursor,
                },
            },
            'second_db': {
                'dbname': 'second_db',
                'user': 'guido',
                'password': 'SuperS3cr!t',
                'host': 'localhost',
                'port': '5432',
                'sslmode': 'disable',
                'application_name': 'myapp',
            },
        }
    """

    def __init__(self, connection_dict, db_alias=DEFAULT_DB_ALIAS):
        self.options = connection_dict.pop('options', {})
        self.isolation_level = self.options.get('isolation_level', ISOLATION_LEVEL_AUTOCOMMIT)
        self.default_cursor_factory = self.options.get('default_cursor_factory', NamedTupleCursor)
        self.connection_dict = connection_dict
        self.name = connection_dict['dbname']
        self.alias = db_alias
        self.conn = None
        databases.register(self)


    @property
    def connection(self):
        """
        An alias for ``Database.conn``.
        """
        return self.conn


    def connect(self):
        """
        Opens a new database connection.
        """
        self.conn = psycopg2.connect(**self.connection_dict)
        self.conn.set_isolation_level(self.isolation_level)
        self.conn.set_client_encoding('UTF8')
        self.conn.cursor_factory = self.default_cursor_factory
        return self.conn




def connect_databases(db_settings):
    """
    Convenience method to connect to all the databases in the ``db_settings``
    argument.

    :param db_settings: A dictionary containing the connection details for
                        each database to connect to. For more information
                        on the value of this argument; check the ``Database``
                        docstring.
    """
    # Validate that the value in db_settings is correct
    dbnames = []
    for db_alias, connection_dict in db_settings.items():
        name = connection_dict.get('dbname')
        if name in dbnames:
            raise ImproperlyConfigured(
                'Same database name in both db connection dictionaries.'
            )
        dbnames.append(name)

    for db_alias, connection_dict in db_settings.items():
        db = Database(connection_dict, db_alias)
        db.connect()
