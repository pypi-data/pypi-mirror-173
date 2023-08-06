pgsql-connection-handler
========================
A package that connects to one or more PostgreSQL databases and allows you
to retrieve a database connection when required. Depends on psycopg2-binary.


Quickstart
----------

1. Install the package:
   ```
   pip install pgsql-connection-handler
   ```

1. Use the package:
   ```python
   from pg_connection_handler import databases, connect_databases

   DATABASES = {
       'default': {
           'dbname': 'mydatabase',
           'user': 'guido',
           'password': 'SuperS3cr!t',
           'host': 'localhost',
           'port': '5432',
           'sslmode': 'disable',
           'application_name': 'myapp',
       },
       'another_db': {
           'dbname': 'mydatabase',
           'user': 'guido',
           'password': 'SuperS3cr!t',
           'host': 'localhost',
           'port': '5432',
           'sslmode': 'disable',
           'application_name': 'myapp',
       },
   }
   connect_databases(DATABASES)

   db_connection = databases.get_connection()

   # Or get the connection based on the alias used in DATABASES
   db_connection = databases.get_connection('db_alias')

   # Or get the database object
   db = databases.get()
   db_connection = db.conn
   ```


Compatiblity
------------
- Compatible with Python 3.8 and above.


Versioning
----------
This project follows [semantic versioning][1] (SemVer).


License, code of conduct and requirements
-----------------------------------------
Check the root of the repo for these files.



[//]: # (Links)

[1]: https://semver.org/
