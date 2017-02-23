import psycopg2
from reddit_saved.sql_databases import PostgresDatabase


class StorageLayer(object):

    def connect(self):
        pass

    def save_row(self, row_seq, **kwargs):
        pass

    def load_row(self, query, query_args, **kwargs):
        pass


class PsqlStorageLayer(StorageLayer):

    def __init__(self):
        self.db = self.connect()

    def connect(self):
        database_info = {'dbname': 'reddit', 'user': 'swoop', 'password': 'password', 'host': 'localhost',
                         'port': '5432'}
        db = PostgresDatabase(database_info)
        db.connect()
        return db

    def save_row(self, value_list, **kwargs):
        self.db.insert_row_to_table(kwargs['table_name'],
                                    value_list,
                                    kwargs['table_column_names_and_types'])


class DjangoStorageLayer(StorageLayer):

    def connect(self):
        pass

