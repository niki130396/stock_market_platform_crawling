from plugins.utils.db_tools import get_from_sql
from plugins.db_connectors import get_db_connection
from os import listdir

connection = get_db_connection()
cursor = connection.cursor()


def create_statement_files():
    files = listdir("/app/tests/queries")
    for file in files:
        if file.startswith("create"):
            yield file


def get_table_name(file_name: str):
    if not file_name.startswith("create"):
        raise ValueError("Can work with create statements only!")
    return file_name[file_name.find("_") + 1:file_name.rfind(".")]


def get_field_names(file_name: str):
    if not file_name.startswith("create"):
        raise ValueError("Can read fields from CREATE statements only!")
    output = []
    with open(f"/app/tests/queries/{file_name}") as file:
        statement = file.read()
        field_definitions = statement[statement.find("(") + 1:statement.rfind(")")].split("\n")
        for field in field_definitions:
            if field and "FOREIGN" not in field:
                field = field.strip()
                output.append(field[:field.find(" ")])
    return ", ".join(output)


def create_table(file_name, data):
    table_name = get_table_name(file_name)
    cursor.execute(f"""DROP TABLE IF EXISTS {table_name}""")
    connection.commit()
    create_sql = get_from_sql(
        file_name,
        path="/app/tests/queries"
    )
    cursor.execute(create_sql)
    connection.commit()
    insert_sql = get_from_sql(
        "insert_into.sql",
        path="/app/tests/queries",
        table_name=table_name,
        fields=get_field_names(file_name),
        row_values=", ".join(["?" for _ in range(len(data[0]))])
    )
    cursor.executemany(insert_sql, data)
    connection.commit()
