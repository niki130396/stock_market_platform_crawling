from plugins.utils.db_tools import get_next_unfetched_ticker
from tests.definitions import DUMMY_DATA
from plugins.utils.common import remove_rows_prior_to_latest
from datetime import datetime
from scrapy_tasks.scrapy_tasks.spiders.stockanalysis_spider import StockAnalysisSpider


def test_arrange_rows_for_insertion(document_dataclass, dummy_stock_analysis_spider):

    arranged_data = StockAnalysisSpider.arrange_rows_for_insertion(
        dummy_stock_analysis_spider,
        DUMMY_DATA,
        document_dataclass
    )
    for row in arranged_data:
        assert isinstance(row, tuple) and None not in row


def test_remove_rows_prior_to_latest(document_dataclass, dummy_stock_analysis_spider):
    arranged_data = StockAnalysisSpider.arrange_rows_for_insertion(
        dummy_stock_analysis_spider,
        DUMMY_DATA,
        document_dataclass
    )
    output = remove_rows_prior_to_latest(arranged_data, document_dataclass.latest_statement_date)

    years = [row[2] for row in output]
    assert min(years) > document_dataclass.latest_statement_date


def test_get_next_unfetched_ticker():
    document = next(get_next_unfetched_ticker())

    now = datetime.now().date()
    assert (now - document.latest_statement_date).days >= 90
