from plugins.utils.db_tools import NormalizedFieldsProcessor, get_next_unfetched_ticker
from tests.definitions import DUMMY_DATA
from plugins.utils.common import remove_rows_prior_to_latest


def arrange_rows_for_insertion(rows, document, normalized_field_processor):
    #  TODO don't keep null values. Just don't write anything in the database instead of keeping a null value.
    output = []
    for i in range(1, len(rows[0])):
        period = rows[0][i]
        for row in rows[1:]:
            field_id = normalized_field_processor.get_normalized_field_id(
                row[0]
            )
            try:
                value = row[i]
            except IndexError:
                continue
            if field_id:
                output.append((document.id, field_id, period, value))
    return output


def test_arrange_rows_for_insertion(document_dataclass):
    normalized_field_processor = NormalizedFieldsProcessor("stock_analysis")

    arranged_data = arrange_rows_for_insertion(DUMMY_DATA, document_dataclass, normalized_field_processor)
    for row in arranged_data:
        assert isinstance(row, tuple) and None not in row


def test_remove_rows_prior_to_latest(document_dataclass):
    normalized_field_processor = NormalizedFieldsProcessor("stock_analysis")
    arranged_data = arrange_rows_for_insertion(DUMMY_DATA, document_dataclass, normalized_field_processor)
    output = remove_rows_prior_to_latest(arranged_data, document_dataclass.latest_statement_date)

    years = [row[2] for row in output]
    assert min(years) > document_dataclass.latest_statement_date


def test_get_next_unfetched_ticker():

    for obj in get_next_unfetched_ticker():
        print(obj.latest_statement_date)
