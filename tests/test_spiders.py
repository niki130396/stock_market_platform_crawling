from plugins.utils.db_tools import get_next_unfetched_ticker
from tests.definitions import DUMMY_DATA, stock_analysis_html_response
from plugins.utils.common import remove_rows_prior_to_latest
from datetime import datetime
from scrapy_tasks.scrapy_tasks.spiders.stockanalysis_spider import StockAnalysisSpider
from scrapy import Request
from scrapy.http import HtmlResponse


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


def test_html_fetch_table(document_dataclass, dummy_stock_analysis_spider):

    request = Request(
                    url="https://stockanalysis.com/stocks/a/financials/quarterly/",
                    meta={"statement_type": "income_statement", "document": document_dataclass},
                    headers={
                        "Accept-Encoding": "gzip, deflate, utf-8",
                        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
                        "Accept": "*/*",
                        "Accept-Language": "en",
                    },
                )
    response = HtmlResponse(url="https://stockanalysis.com/stocks/a/financials/quarterly/",
                            request=request,
                            body=stock_analysis_html_response,
                            encoding="utf-8"
                            )
    rows = StockAnalysisSpider.get_rows(dummy_stock_analysis_spider, response, "income_statement")
    dates = StockAnalysisSpider.get_dates(response)
    assert dates[0] == "2022-06-30" and dates[-1] == "2012-09-30"
    assert rows[0][0] == "total_revenue" and rows[0][-1] == 1723
    for item in rows[1][1:]:
        assert type(item) == int
