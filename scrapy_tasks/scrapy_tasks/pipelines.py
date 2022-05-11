# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from plugins.utils.db_tools import insert_financial_statement_item
from plugins.utils.db_tools import (
    update_statement_type_availability,
    update_ticker_status
)


class FinancialStatementPipeline:
    def process_item(self, item, spider):
        item = dict(item)
        if item["data"]:
            insert_financial_statement_item(item["data"])
            update_statement_type_availability(
                item["metadata"]["statement_type"], item["metadata"]["symbol"]
            )
            update_ticker_status(
                item["metadata"]["symbol"],
                item["metadata"]["latest_statement_date"],
            )
        return item
