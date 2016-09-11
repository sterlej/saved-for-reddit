import psycopg2
from reddit_saved.sql_databases import PostgresDatabase


class SearchLayer(object):

    def search(self, query, parameters):
        pass


class PsqlSearchLayer(object):

    def search(self, query, parameters):
        pass
