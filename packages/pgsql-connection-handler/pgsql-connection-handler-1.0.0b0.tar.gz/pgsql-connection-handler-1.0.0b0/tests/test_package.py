import pytest

from pg_connection_handler import databases, connect_databases
from pg_connection_handler.exceptions import (
    ImproperlyConfigured,
    ConnectionDoesNotExist,
)



DATABASES = {
    'default': {
       'dbname': 'connection_handler',
       'user': 'postgres',
       'password': 'password',
       'host': 'localhost',
       'port': '5432',
       'sslmode': 'disable',
       'application_name': 'pgsql-connection-handler',
    },
}



def test_connect():
    connect_databases(DATABASES)
    db_connection = databases.get_connection()
    assert db_connection.closed == 0
    databases.reset()



def test_connect_if_closed():
    connect_databases(DATABASES)
    db_connection = databases.get_connection()
    db_connection.close()
    assert db_connection.closed > 0
    db_connection = databases.get_connection()
    assert db_connection.closed == 0
    databases.reset()



def test_close():
    connect_databases(DATABASES)
    databases.close()
    connection = databases.get_connection(reconnect_if_closed=False)
    assert connection.closed > 0
    databases.reset()



def test_get_db():
    connect_databases(DATABASES)
    db = databases.get()
    assert db.conn.closed == 0
    assert db.name == 'connection_handler'
    databases.reset()



def test_connection_alias():
    connect_databases(DATABASES)
    db = databases.get()
    assert db.conn == db.connection
    databases.reset()



def test_close_all():
    connect_databases(DATABASES)
    db_connection = databases.get_connection()
    databases.close_all()
    assert db_connection.closed > 0
    databases.reset()



def test_bad_config():
    test_dict = {
        'default': {
           'dbname': 'connection_handler',
           'user': 'postgres',
           'password': 'password',
           'host': 'localhost',
           'port': '5432',
           'sslmode': 'disable',
           'application_name': 'pgsql-connection-handler',
        },
        'default2': {
           'dbname': 'connection_handler',
           'user': 'postgres',
           'password': 'password',
           'host': 'localhost',
           'port': '5432',
           'sslmode': 'disable',
           'application_name': 'pgsql-connection-handler',
        },
    }
    with pytest.raises(ImproperlyConfigured):
        connect_databases(test_dict)
    databases.reset()



def test_connection_does_not_exist():
    connect_databases(DATABASES)
    with pytest.raises(ConnectionDoesNotExist):
        databases.get_connection('nonexistent')
    databases.reset()
