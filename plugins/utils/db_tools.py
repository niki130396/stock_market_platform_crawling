import os
from collections import defaultdict

import psycopg2
from jinja2 import Template
from psycopg2.extras import execute_values
from plugins.utils.models import DocumentModel
from plugins.db_connectors import get_db_connection


connection = get_db_connection()
cursor = connection.cursor()


def get_from_sql(file_name: str, path=None, **kwargs):
    name, extension = file_name.split(".")
    if extension != "sql":
        raise ValueError("Only .sql extension files supported")
    if not path:
        current_file_path = os.path.dirname(__file__)
        abs_file_path = os.path.join(current_file_path, file_name)
    else:
        abs_file_path = os.path.join(path, file_name)
    with open(abs_file_path, "r") as sql_file:
        SQL = Template(sql_file.read()).render(**kwargs)
        return SQL


def insert_financial_statement_item(data):
    SQL = get_from_sql("query_statements/insert_financial_statement_fact.sql")
    execute_values(cursor, SQL, data)


def get_next_unfetched_ticker():
    SQL = get_from_sql("query_statements/select_next_ticker_for_processing.sql")
    while True:
        cursor.execute(SQL)
        row = cursor.fetchone()
        yield DocumentModel(
            id=row[0],
            symbol=row[1],
            name=row[2],
            sector=row[7],
            industry=row[8],
            latest_statement_date=row[15]
        )


def update_ticker_status(symbol, latest_statement_date):
    SQL = get_from_sql(
        "query_statements/update_ticker_is_available.sql",
        symbol=symbol,
        latest_statement_date=latest_statement_date,
    )
    cursor.execute(SQL)


def update_statement_type_availability(statement_type, symbol):
    SQL = get_from_sql(
        f"query_statements/set_{statement_type}_availability.sql", symbol=symbol
    )
    cursor.execute(SQL)


def get_unfetched_objects():
    SQL = get_from_sql("query_statements/select_unfetched_statements.sql")
    cursor.execute(SQL)
    output = []
    for row in cursor.fetchall():
        output.append(
            DocumentModel(
                id=row[0], symbol=row[1], name=row[2], sector=row[7], industry=row[8], latest_statement_date=row[15]
            )
        )
    return output


def get_source_statement_types_map():
    SQL = get_from_sql("query_statements/source_statement_types.sql")
    statements_map = {}

    cursor.execute(SQL)
    for row in cursor.fetchall():
        statements_map[row[1]] = row[0]
    return statements_map


class NormalizedFieldsProcessor:
    def __init__(self, source_name):
        self.__source_name = source_name
        self.__mapped_fields = self.fetch_source_and_normalized_field_names()
        self.__mapped_normalized_field_ids = self.fetch_normalized_field_to_field_id()

    @staticmethod
    def fetch_fields():
        output = defaultdict(dict)
        for fields in cursor.fetchall():
            source_field_name, local_field_name, local_statement_type_name = fields
            output[local_statement_type_name].update(
                {source_field_name: local_field_name}
            )
        if not output:
            raise psycopg2.DataError(
                "Either the source name is wrong or there are no associated field attributes"
                "to the given source name"
            )
        return output

    def fetch_source_and_normalized_field_names(self):
        output = {}
        cursor.execute(
            get_from_sql(
                "query_statements/normalized_fields.sql",
                source_name=self.__source_name,
            )
        )
        output.update(self.fetch_fields())
        return output

    def fetch_normalized_field_to_field_id(self):
        output = {}
        cursor.execute(
            get_from_sql(
                "query_statements/normalized_field_to_field_id.sql",
                source_name=self.__source_name,
            )
        )
        normalized_fields = list(cursor.fetchall())
        for field_name, field_id in normalized_fields:
            output[field_name] = field_id
        return output

    def get_local_field(self, statement_type: str, source_field: str):
        if source_field in self.__mapped_fields[statement_type]:
            return self.__mapped_fields[statement_type][source_field]

    def get_normalized_field_id(self, normalized_field: str):
        if normalized_field in self.__mapped_normalized_field_ids:
            return self.__mapped_normalized_field_ids[normalized_field]
