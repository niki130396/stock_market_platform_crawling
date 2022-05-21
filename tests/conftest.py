
import pytest
from tests.create_tables import (
        create_table,
)
from tests.definitions import (
        COMPANY,
        SOURCE_DETAILS,
        STATEMENT_FACT,
        STATEMENT_LINE,
        STATEMENT_TYPE,
        NORMALIZED_FIELDS,
)
from plugins.utils.models import DocumentModel
from plugins.utils.db_tools import NormalizedFieldsProcessor


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    create_table("create_financial_statements_statementsmetadata.sql", COMPANY)

    create_table("create_crawling_crawlingsourcedetails.sql", SOURCE_DETAILS)

    create_table("create_crawling_normalizedfieldtree.sql", NORMALIZED_FIELDS)

    create_table("create_crawling_statementtypelocaldefinition.sql", STATEMENT_TYPE)

    create_table("create_crawling_financialstatementline.sql", STATEMENT_LINE)

    create_table("create_crawling_financialstatementfact.sql", STATEMENT_FACT)


@pytest.fixture
def document_dataclass():
    return DocumentModel(
            id=COMPANY[0][0],
            symbol=COMPANY[0][1],
            name=COMPANY[0][2],
            sector=COMPANY[0][7],
            industry=COMPANY[0][8],
            latest_statement_date=COMPANY[0][15]
        )


@pytest.fixture
def dummy_stock_analysis_spider():
    class Spider:
        def __init__(self):
            self.normalized_field_processor = NormalizedFieldsProcessor("stock_analysis")

    obj = Spider()
    return obj
