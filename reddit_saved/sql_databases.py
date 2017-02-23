import psycopg2
import psycopg2.extras
import ast
import json
from datetime import datetime


class PostgresFullTextSyntax(object):

    def __init__(self, column, query, ptype):
        tsvector = "to_tsvector('english', \""
        tsquery = "to_tsquery('english', "
        plain_tsquery = "plainto_tsquery('english', "
        rank = 'ts_rank_cd('

        # create mulit word if space exists in query
        if ptype is not 'relative' and ' ' in query:
            originalQuery = query
            query = ''
            for word in originalQuery.split():
                query += word + ' &'
            query = query[:-2]

        self.vector = tsvector + column + '")'
        self.query = tsquery + "%s)"
        self.plain_query = plain_tsquery + "%s)"
        self.ts_rank = rank + self.vector + ', ' + self.query + ', 2|32)'


class SqlDatabase(object):

    def __init__(self, database_info):
        '''
        :param database_info - dictionary; keys = [dbname, user, password, host, port]:
        '''
        self.database_info = database_info
        self.connection = None
        self.cursor = None

    def connect(self):
        if 'NAME' in self.database_info:
            db_name = self.database_info['NAME']
        else:
            db_name = self.database_info['dbname']

        print("Cannot connect to '{0}' of type {1}".format(db_name, self.database_info['type']))

    def disconnect(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()

    def execute(self, sql, args=(), dict_cursor=False):
        pass

    def fetch(self, clean_data=True):
        cleaned_data = None

        if self.cursor:
            try:
                fetched = self.cursor.fetchall()
                if clean_data:
                    cleaned_data = self.__parse_fetched_data(fetched)
                else:
                    cleaned_data = fetched
                self.cursor.close()
                self.cursor = None
            except:
                cleaned_data = None

        return cleaned_data

    def __parse_fetched_data(self, fetched_data):
        cleaned_fetched_data = None

        if len(fetched_data) == 1 and len(fetched_data[0]) == 1:
            cleaned_fetched_data = fetched_data[0][0]

        elif len(fetched_data) > 1 and len(fetched_data[0]) == 1 and len(fetched_data[0][0]) > 1:
            data_list = []
            [data_list.append(data[0]) for data in fetched_data]
            cleaned_fetched_data = tuple(data_list)

        elif len(fetched_data) > 1:
            cleaned_fetched_data = fetched_data

        elif len(fetched_data) == 1 and len(fetched_data[0]) > 1:
            cleaned_fetched_data = fetched_data[0]

        return cleaned_fetched_data

    def create_table(self, table_name, column_tuples):
        sql = 'CREATE TABLE "' + table_name + '" ('
        for tuples in column_tuples:
            name = tuples[0].replace(' ', '_')

            pg_type = tuples[1]
            if name == 'id':
                pg_type += ' primary key'
            sql = sql + name + ' ' + pg_type + ', '
        sql = sql[:-2] + ');'
        self.execute(sql)

    def drop_table(self, table_name):
        sql = "DROP TABLE IF EXISTS {0}".format(table_name)
        self.execute(sql)

    def drop_column(self, table_name, column_name):
        sql = 'ALTER TABLE "{0}" DROP COLUMN "{1}";'.format(table_name, column_name)
        self.execute(sql)

    def add_column(self, table_name, column_name, column_type):
        sql = 'ALTER TABLE "{0}" ADD COLUMN "{1}" {2};'.format(table_name, column_name, column_type)
        self.execute(sql)

    def get_record_count(self, table_name, execute_sql=True):

        sql = 'SELECT COUNT(*) FROM "{0}";'.format(table_name)

        if execute_sql:
            self.execute(sql)
            record_count = self.fetch()
            return float(record_count)
        else:
            return sql

    def get_record_by_id(self, table_name, id_column, id_value, execute_sql=True):

        sql = 'SELECT * FROM "{0}" WHERE "{1}" = %s;'.format(table_name, id_column)

        if execute_sql:
            self.execute(sql, (id_value,))
            record = self.fetch()
            return record
        else:
            return sql

    def get_column_names_types(self, table_name, execute_sql=True):

        sql = "SELECT column_name, data_type, udt_name FROM information_schema.columns " \
              "WHERE table_name ='{0}';".format(table_name)

        if execute_sql:
            self.execute(sql)
            column_names_types = self.fetch()
            return column_names_types
        else:
            return sql

    def get_column_names(self, table_name, execute_sql=True):

        sql = 'SELECT column_name FROM information_schema.columns WHERE table_name =\'{0}\';'.format(table_name)

        if execute_sql:
            self.execute(sql)
            column_names = self.fetch()
            return column_names
        else:
            return sql

    def get_column_range(self, column, table_name):
        column_range = []

        min_sql = 'SELECT MIN("{0}") FROM "{1}";'.format(column, table_name)
        self.execute(min_sql)
        min_val = self.fetch()

        max_sql = 'SELECT MAX("{0}") FROM "{1}";'.format(column, table_name)
        self.execute(max_sql)
        max_val = self.fetch()

        column_range = [str(min_val), str(max_val)]

        return column_range

    def compute_column_coverage(self, record_count, column, table_name, execute_sql=True):

        sql = 'SELECT COUNT("{0}") FROM "{1}";'.format(column, table_name)

        if execute_sql:
            self.execute(sql)
            total_count = self.fetch()
            coverage = total_count/record_count
            return coverage
        else:
            return sql

    def compute_column_variability(self, record_count, column, table_name, execute_sql=True):

        sql = 'SELECT COUNT(DISTINCT "{0}") FROM "{1}";'.format(column, table_name)

        if execute_sql:
            self.execute(sql)
            distinct_count = self.fetch()
            variability = distinct_count/record_count
            return variability
        else:
            return sql

    def compute_column_average_field_length(self, column, table_name, execute_sql=True):

        sql = 'SELECT AVG(LENGTH("{0}")) FROM "{1}";'.format(column, table_name)

        if execute_sql:
            self.execute(sql)
            average_field_length = self.fetch()
            return float(average_field_length)
        else:
            return sql

    def compute_column_mean(self, column, table_name, execute_sql=True):

        sql = 'SELECT AVG("{0}") FROM "{1}";'.format(column, table_name)

        if execute_sql:
            self.execute(sql)
            mean = self.fetch()
            return float(mean)
        else:
            return sql

    def select_geo(self, latitude_column, longitude_column, return_column, table_name,
                   latitude_min, latitude_max, longitude_min,longitude_max, execute_sql=True):

        sql = 'SELECT "{0}" FROM "{1}" WHERE ("{2}" BETWEEN %s AND %s) AND ("{3}" BETWEEN %s AND %s);'.format(return_column,
                                                                                                      table_name,
                                                                                                      latitude_column,
                                                                                                      longitude_column)

        if execute_sql:
            self.execute(sql, (latitude_min, latitude_max, longitude_min, longitude_max))
            return self.fetch()
        else:
            return sql

    def select_equals(self, select_column, return_column, table_name, value, execute_sql=True, clean=True):

        sql = 'SELECT "{0}" FROM "{1}" WHERE "{2}" = %s;'.format(return_column, table_name, select_column)

        if execute_sql:
            self.execute(sql, (value,))
            return self.fetch(clean_data=clean)
        else:
            return sql

    def select_between(self, select_column, return_column, table_name, min_val, max_val, execute_sql=True):

        sql = 'SELECT "{0}" FROM "{1}" WHERE "{2}" BETWEEN %s AND %s;'.format(return_column, table_name, select_column)

        if execute_sql:
            self.execute(sql, (min_val, max_val))
            return self.fetch()
        else:
            return sql

    def select_greater_than(self, select_column, return_column, table_name, min_val, execute_sql=True):

        sql = 'SELECT "{0}" FROM "{1}" WHERE "{2}" >= %s;'.format(return_column, table_name, select_column)

        if execute_sql:
            self.execute(sql, (min_val,))
            return self.fetch()
        else:
            return sql

    def select_less_than(self, select_column, return_column, table_name, max_val, execute_sql=True):

        sql = 'SELECT "{0}" FROM "{1}" WHERE "{2}" <= %s;'.format(return_column, table_name, select_column)

        if execute_sql:
            self.execute(sql, (max_val,))
            return self.fetch()
        else:
            return sql

    def select_like(self, select_column, return_column, table_name, value, execute_sql=True):

        sql = 'SELECT "{0}" FROM "{1}" WHERE "{2}" LIKE %(like)s ;'.format(return_column, table_name, select_column)
        if execute_sql:
            self.execute(sql, dict(like='%'+value+'%'))
            return self.fetch(clean_data=False)
        else:
            return sql

    def select_like_after(self, select_column, return_column, table_name, value, execute_sql=True):

        sql = 'SELECT "{0}" FROM "{1}" WHERE "{2}" LIKE %(like)s ;'.format(return_column, table_name, select_column)
        if execute_sql:
            self.execute(sql, dict(like='%'+value))
            return self.fetch(clean_data=False)
        else:
            return sql

    def select_like_before(self, select_column, return_column, table_name, value, execute_sql=True):

        sql = 'SELECT "{0}" FROM "{1}" WHERE "{2}" LIKE %(like)s ;'.format(return_column, table_name, select_column)
        if execute_sql:
            self.execute(sql, dict(like=value+'%'))
            return self.fetch(clean_data=False)
        else:
            return sql

    def select_most_recent_date(self, date_column, table_name, execute_sql=True):

        sql = 'SELECT "{0}" FROM "{1}" ORDER BY "{0}" DESC LIMIT 1;'.format(date_column, table_name)

        if execute_sql:
            self.execute(sql, ())
            return self.fetch()
        else:
            return sql


class PostgresDatabase(SqlDatabase):

    def __init__(self, database_info):
        super(PostgresDatabase, self).__init__(database_info)

    def connect(self):
        dbname = self.database_info['dbname']
        user = self.database_info['user']
        password = self.database_info['password']
        host = self.database_info['host']
        port = self.database_info['port']

        try:
            connection = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
        except psycopg2.Error as e:
            connection = None
            print(e.pgerror)

        self.connection = connection

    def execute(self, sql, args=(), dict_cursor=False):
        if self.connection:

            if dict_cursor:
                self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            else:
                self.cursor = self.connection.cursor()

            try:
                self.cursor.execute(sql, args)
            except psycopg2.Error as e:
                print(sql, args)
                print(e.pgerror)
            except Exception as e:
                print(e.message)

            self.connection.commit()

        elif 'dbname' not in self.database_info:
            print("\nDatabase '{0}' is not connected. Execute failed.".format(self.database_info['NAME']))
        else:
            print("\nDatabase '{0}' is not connected. Execute failed.".format(self.database_info['dbname']))

    def copy_csv_to_table(self, table_name, csv_file):
        if self.connection:
            cursor = self.connection.cursor()

            sql = "COPY \"{0}\" FROM STDIN WITH Delimiter ',' CSV;".format(table_name)
            with open(csv_file) as copy_csv:
                cursor.copy_expert(sql=sql, file=copy_csv)
            self.connection.commit()

        elif 'dbname' not in self.database_info:
            print("\nDatabase '{0}' is not connected. Copy csv failed.".format(self.database_info['NAME']))
        else:
            print("\nDatabase '{0}' is not connected. Copy csv failed.".format(self.database_info['dbname']))

    def insert_row_to_table_from_shape(self, table_name, row, columns_and_types):
        psql_column_string = '('
        row_string = '('
        columns, types = zip(*columns_and_types)

        #Add geo function to any geometry fields
        for i, value in enumerate(row):
            if types[i] == 'geometry':
                row_string += "ST_GeomFromText(%s), "
            else:
                row_string += '%s, '
            psql_column_string += columns[i] + ', '

        psql_column_string = psql_column_string[:-2] + ')'
        row_string = row_string[:-2] + ')'

        sql = "INSERT INTO \"{0}\" {1} VALUES {2};".format(table_name, psql_column_string, row_string)
        self.execute(sql, tuple(row))

    def insert_row_to_table(self, table_name, row, columns_and_types):
        psql_column_string = '('
        row_string = '('
        columns, types = zip(*columns_and_types)

        #Add geo function to any geometry fields
        for i, value in enumerate(row):
            row_string += '%s, '
            psql_column_string += columns[i] + ', '

        psql_column_string = psql_column_string[:-2] + ')'
        row_string = row_string[:-2] + ')'

        sql = "INSERT INTO \"{0}\" {1} VALUES {2};".format(table_name, psql_column_string, row_string)
        self.execute(sql, tuple(row))

    def compute_column_standard_deviation_population(self, column, table_name, execute_sql=True):

        sql = 'SELECT STDDEV_POP("{0}") FROM "{1}";'.format(column, table_name)

        if execute_sql:
            self.execute(sql)
            standard_dev = self.fetch()
            return float(standard_dev)
        else:
            return sql

    def index_column(self, column_name_type, table_name, execute_sql=True):
        column_name = column_name_type[0]
        column_type = column_name_type[1]

        begin_sql = 'CREATE INDEX \"swoop-{0}-{1}\" ON "{0}" '.format(table_name, column_name)

        if column_type == 'text':
            end_sql = 'USING gin(to_tsvector(\'english\', "{0}"));'.format(column_name)
        else:
            end_sql = '("{0}")'.format(column_name)

        sql = begin_sql + end_sql

        if execute_sql:
            self.execute(sql)
        else:
            return sql

    def drop_all_tables(self):
        select_sql = 'select \'drop table if exists "\' || tablename || \'" cascade;\' from pg_tables where schemaname = \'public\';'
        self.execute(select_sql)
        drop_statements = self.fetch()

        if isinstance(drop_statements, str):
            drop_statements = [drop_statements]

        if drop_statements:
            for sql in drop_statements:
                if 'spatial_ref_sys' not in sql: #Don't drop postgis table
                    self.execute(sql)

    def get_tablenames(self, table_name=None, clean=True):

        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' " \
              "AND table_type='BASE TABLE'"

        if table_name:
            sql += "AND table_name='{0}';".format(table_name)

        self.execute(sql)
        table_names = self.fetch(clean)

        return table_names

    def get_tablenames_like(self, table_name):

        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' " \
              "AND table_type='BASE TABLE' AND table_name LIKE %(like)s;"
        self.execute(sql, dict(like='%'+table_name+'%'))
        table_names = self.fetch(clean_data=False)

        return table_names

    def get_tablenames_like_before(self, table_name):

        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' " \
              "AND table_type='BASE TABLE' AND table_name LIKE %(like)s;"
        self.execute(sql, dict(like=table_name+'%'))
        table_names = self.fetch(clean_data=False)

        return table_names

    def get_tablenames_like_after(self, table_name):

        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' " \
              "AND table_type='BASE TABLE' AND table_name LIKE %(like)s;"
        self.execute(sql, dict(like='%'+table_name))
        table_names = self.fetch(clean_data=False)

        return table_names

    def get_table_size(self, table_name, execute_sql=True):

        sql = "SELECT pg_size_pretty(pg_total_relation_size('\"{0}\"'));".format(table_name)

        if execute_sql:
            self.execute(sql)
            table_size= self.fetch()
            return table_size
        else:
            return sql

    def get_first_value(self, column, table_name, execute_sql=True):

        sql = 'SELECT COALESCE("{0}") FROM "{1}" LIMIT 1;'.format(column, table_name)

        if execute_sql:
            self.execute(sql)
            first_value = self.fetch()
            return first_value
        else:
            return sql

    def full_text_search(self, select_column, return_column, table_name, value, rank, param_type=None, execute_sql=True):

        ft_syntax = PostgresFullTextSyntax(select_column, value, param_type)

        if rank:
            sql = 'SELECT "{0}", {1} as rank FROM "{2}" WHERE {3} @@ {4};'.format(return_column, ft_syntax.ts_rank,
                                                                                 table_name, ft_syntax.vector,
                                                                                 ft_syntax.query)
        else:
            sql = 'SELECT "{0}" FROM "{1}" WHERE {2} @@ {3};'.format(return_column, table_name, ft_syntax.vector,
                                                                       ft_syntax.query)

        if execute_sql:
            self.execute(sql, (value, value))
            return self.fetch()
        else:
            return sql

    def select_mac_trunc(self, select_column, return_column, table_name, value, execute_sql=True):

        sql = 'SELECT "{0}" FROM "{1}" WHERE trunc("{2}") = trunc(macaddr %s);'.format(return_column, table_name, select_column)

        if execute_sql:
            self.execute(sql, (value,))
            return self.fetch()
        else:
            return sql

    def select_network(self, select_column, return_column, table_name, value, execute_sql=True):
        value += '/24'
        sql = 'SELECT "{0}" FROM "{1}" WHERE "{2}" <<= %s;'.format(return_column, table_name, select_column)

        if execute_sql:
            self.execute(sql, (value,))
            return self.fetch()
        else:
            return sql

    def select_geo(self, select_column, second_select_column, return_column, table_name,
                   latitude_min, latitude_max, longitude_min,longitude_max, execute_sql=True):

        # ASSUMES record geometry is stored in 'geom' field (which is standard for shapefiles)
        sql = 'SELECT "{0}" from "{1}" WHERE "{2}" && ST_MakeEnvelope(%s, %s, %s, %s, 4326);'.format(return_column,
                                                                                               table_name, select_column)

        if execute_sql:
            self.execute(sql, (longitude_min, latitude_min, longitude_max, latitude_max))
            return self.fetch()
        else:
            return sql

    def vaccuum_analyze(self, db_name):
        sql = "VACCUUM ANALYZE \"{0}\";".format(db_name)
        self.execute(sql)

    '''
    Postgis functions
    '''
    def point_to_geometry(self, latitude_value, longitude_value, execute_sql=True):
        sql = "SELECT ST_MakePoint(%s, %s);"

        if execute_sql:
            self.execute(sql, (longitude_value, latitude_value))
            return self.fetch()
        else:
            return sql


