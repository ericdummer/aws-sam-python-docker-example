import psycopg2
import psycopg2.errors as pg_errors
import psycopg2.extras
import psycopg2.pool 
import json
import os
import boto3


from services.secrets_service import SecretsService  # Assuming the previous class is available
from botocore.exceptions import ClientError

class DbService:

    DEFAULT_BATCH_SIZE  = 1000
    _instance = None
    database = None
    _connection = None
    secrets_helper:SecretsService = None
    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, database = None, secret_arn = None):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

            if (database is None):
                database = os.environ.get("DATABASE_NAME")
            cls._instance.database = database

            if (secret_arn is None):
                secret_arn = os.environ.get('SECRET_ARN') 
            cls._instance.secrets_helper = SecretsService(secret_arn)
        return cls._instance
    
    def get_connection(self):
        """Connects to the database."""
        if self._connection is not None:
            return self._connection
        # Retrieve connection info from secret manager
        try:
            db_host = self.secrets_helper.get_secret_value('DB_HOST') 
            user = self.secrets_helper.get_secret_value('DB_USER')
            password = self.secrets_helper.get_secret_value('DB_PASSWORD')

            connection_info = {
                "host": db_host,
                "user": user, 
                "database": self.database,
                "password" : password
            }  # To store retrieved connection details
        except (ValueError, ClientError) as e:
            raise Exception(f"Error retrieving connection info: {e}") from e

        # Use retrieved connection info to establish connection
        try:
            self._connection = psycopg2.connect(**connection_info, connect_timeout=2)
            return self._connection
        except (Exception, pg_errors.Error) as error:
            raise Exception(f"Error connecting to database: {error}") from error


    def get_query_result(self, query, params=None):
        """Executes a query and returns the result."""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    if params is None:
                        cur.execute(query)
                        result = cur.fetchall()  # Get the result
                    else:
                        params = tuple(params)  # Convert list to tuple if necessary
                        # print(f"Executing query: {query}, with params: {params}")  # Debugging output
                        cur.execute(query, params)
                        result = cur.fetchall()  # Get the result
                        cur.close()
            return result
        except (Exception, pg_errors.Error) as error:
            raise Exception(f"Error executing query: {error}") from error

    def get_count(self, query, params = None):
        count = 0
        wrapped = f"SELECT count(1) as total FROM ({query}) t"
        results = self.get_query_result(wrapped, params)
        for row in results:
            count = row['total']
        return count

    def execute_query(self, query, params=None):
        """Executes a query and returns the number of updated records."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    updated_records = cur.rowcount  # Get the number of updated records
            return updated_records
        except (Exception, pg_errors.Error) as error: 
            raise Exception(f"Error executing query: {error}") from error
        
    
        
    def insert_data(self, table_name, data):
        columns = data.keys()
        placeholders = ", ".join(["%s"] * len(columns))
        column_str = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({column_str}) VALUES ({placeholders})"
        values = tuple(data.values())  # Convert to tuple for psycopg2
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, values)
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
            raise error


    def upsert_data(self, table_name, conflict_column, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        conflict_target = f'({conflict_column})'  # Or a list of columns like '("col1", "col2")'

        sql = f"""
            INSERT INTO {table_name} ({columns}) 
            VALUES ({placeholders})
            ON CONFLICT {conflict_target} 
            DO UPDATE SET {','.join([f"{col} = EXCLUDED.{col}" for col in data.keys()])}
        """
        try:
            with self.get_connection() as conn:
                print ("CONNECTION: ")
                print (conn)
                with conn.cursor() as cursor:
                    cursor.execute(sql, list(data.values())) 
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            with self.get_connection() as conn:
                conn.rollback()
            raise error

    def update_table(self, table_name, data, where_clause, where_params):
        """
        Updates a row in a PostgreSQL table with a flexible WHERE clause.

        Args:
            conn: An active PostgreSQL database connection.
            table_name (str): The name of the table to update.
            data (dict): A dictionary containing columns and values to update.
            where_clause (str): The WHERE clause of the update query 
                                (e.g., "id = %s").
            where_params (list or tuple):  Parameters for the WHERE clause.
        """

        # Remove 'id' if present (assuming 'id' is your primary key)
        record_id = data.pop('id', None)

        columns_and_values = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table_name} SET {columns_and_values} WHERE {where_clause}"

        values = list(data.values())

        # Add where_params, and potentially record_id if it was removed
        if record_id is not None:
            values.append(record_id)
        values.extend(where_params)

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, list(data.values())) 
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
            raise error
        
    def get_batch(self, sql, params, page = 1, page_size = None):

        if page_size is None:
            page_size = self.DEFAULT_BATCH_SIZE
        offset = (page - 1) * page_size
        limit_query = f"""{sql}
                LIMIT {page_size} OFFSET {offset}"""
        self.logger.debug(f"Getting batch: LIMIT {page_size} OFFSET {offset}")
        self.logger.debug(limit_query)
        return self.get_query_result(limit_query, params)