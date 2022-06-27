from datetime import datetime
from scrapy.exceptions import CloseSpider
from scrapy.http import Request

from scrapy_tasks.scrapy_tasks.base_spiders import FinancialStatementCrawlSpider  # noqa F401
from scrapy_tasks.scrapy_tasks.items import FinancialStatementItem  # noqa F401

from plugins.utils.common import (
    parse_numeric_string,
    convert_to_normalized_quarter,
    remove_rows_prior_to_latest,
)
from plugins.utils.db_tools import get_next_unfetched_ticker


class StockAnalysisSpider(FinancialStatementCrawlSpider):
    name = "stock_analysis_spider"
    handle_httpstatus_list = [200, 429]
    source_name = "stock_analysis"
    income_statement_source_definition = ("", "income_statement")
    balance_sheet_statement_source_definition = ("balance-sheet", "balance_sheet")
    cash_flow_statement_source_definition = ("cash-flow-statement", "cash_flow")

    @staticmethod
    def build_url(symbol: str, statement_type: str):
        url = f"https://stockanalysis.com/stocks/{symbol.lower()}/financials/"
        if statement_type:
            url += statement_type + "/"
        url += "quarterly/"
        return url

    def start_requests(self):
        for obj in get_next_unfetched_ticker():

            for source_statement_type, local_statement_type in (
                self.income_statement_source_definition,
                self.balance_sheet_statement_source_definition,
                self.cash_flow_statement_source_definition,
            ):
                url = self.build_url(obj.symbol, source_statement_type)
                yield Request(
                    url=url,
                    callback=self.parse,
                    meta={"statement_type": local_statement_type, "document": obj},
                    headers={"Accept-Encoding": "gzip, deflate, utf-8"},
                )

    def parse(self, response, **kwargs):
        if response.status == 429:
            raise CloseSpider(
                reason="Spider is blacklisted and we will have to give it some time out"
            )

        document = response.meta.get("document")
        local_statement_type = response.meta.get("statement_type")

        table_data = []
        header = self.get_dates(response)
        table_data.append(header)
        rows = self.get_rows(response, local_statement_type)
        table_data.extend(rows)
        rows_to_insert = self.arrange_rows_for_insertion(table_data, document)
        latest_rows = remove_rows_prior_to_latest(rows_to_insert, document.latest_statement_date)

        item = FinancialStatementItem()
        item["metadata"] = response.meta.get("document").__dict__
        item["metadata"]["statement_type"] = local_statement_type
        item["metadata"]["latest_statement_date"] = rows[0][1]
        item["data"] = latest_rows
        yield item

    def get_rows(self, response, statement_type):
        parsed_rows = []
        table = response.xpath("//tbody//tr")

        if table:
            for row in table:
                elements = row.xpath("./td")
                row_values = []
                row_name = elements[0].xpath(".//span/text()[1]").get()

                normalized_row_name = self.normalized_field_processor.get_local_field(
                    statement_type, row_name
                )
                if not normalized_row_name:
                    continue

                row_values.append(normalized_row_name)
                for el in elements[1:]:
                    value = el.xpath("./text()[1]").get()
                    if value:
                        row_values.append(parse_numeric_string(value))

                while isinstance(row_values[-1], str):
                    row_values.pop()

                parsed_rows.append(row_values)
        return parsed_rows

    @staticmethod
    def get_dates(response):
        output = []
        years = response.xpath("//thead//th")
        if years:
            element = years[0]
            value = element.xpath(".//span/text()[1]").get()
            if value:
                output.append(value)

            for element in years[1:]:
                value = element.xpath("./text()[1]").get()
                if value:
                    try:
                        date = convert_to_normalized_quarter(
                            datetime.strptime(value, "%Y-%m-%d")
                        )
                        output.append(date)
                    except ValueError:
                        continue
        return output

    def arrange_rows_for_insertion(self, rows, document):
        output = []
        for i in range(1, len(rows[0])):
            period = rows[0][i]
            for row in rows[1:]:
                field_id = self.normalized_field_processor.get_normalized_field_id(
                    row[0]
                )
                try:
                    value = row[i]
                except IndexError:
                    continue
                if field_id:
                    output.append((document.id, field_id, period, value))
        return output
