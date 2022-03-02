# import sys
# import time
# from collections import deque
# from os import environ
#
# from scrapy.spiders import CrawlSpider
# from scrapy_tasks.items import FinancialStatementItem
# from scrapy_tasks.requests import SeleniumRequest
# from selenium.webdriver.common.by import By
#
# sys.path.insert(0, f"{environ['AIRFLOW_HOME']}/plugins/")
# from utils.db_tools import (  # noqa E402
#     NormalizedFieldsProcessor,
#     get_company_id,
#     get_next_unfetched_ticker,
#     get_source_statement_types_map,
#     map_normalized_field_to_field_id,
# )
# from utils.models import DocumentModel  # noqa E402
# from utils.selenium_helpers import element_exists  # noqa E402
#
#
# # TODO might have to use splash and scrapy-splash to get collapse items from statements
# class YahooFinanceStatementsSpider(CrawlSpider):
#     name = "yahoo_finance_statements_spider"
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.source_name = "yahoo_finance"
#
#     def __build_url(self, symbol, statement_type):
#         return f"https://finance.yahoo.com/quote/{symbol}/{statement_type}?p={symbol}"
#
#     def start_requests(self):
#         self.fields_processor = NormalizedFieldsProcessor(self.source_name)
#         self.normalized_fields = self.fields_processor.mapped_source_fields
#         self.local_statement_types = {
#             v: k for k, v in get_source_statement_types_map().items()
#         }
#         self.normalized_field_to_field_id_map = map_normalized_field_to_field_id(
#             self.source_name
#         )
#         self.company_id_queue = deque()
#
#         for obj in get_next_unfetched_ticker():
#             company_id = get_company_id(obj.symbol)
#             urls = []
#             for statement_type in ("financials", "balance-sheet", "cash-flow"):
#                 urls.append(
#                     (self.__build_url(obj.symbol, statement_type), statement_type, obj)
#                 )
#                 self.company_id_queue.append(company_id)
#             for url, statement_type, document in urls:
#                 yield SeleniumRequest(
#                     url=url,
#                     callback=self.parse,
#                     meta={"statement_type": statement_type, "document": document},
#                     # script="document.getElementsByClassName('btn primary')[0].click()",
#                     # wait_time=2
#                 )
#                 time.sleep(4)
#
#     def parse(self, response, **kwargs):
#         driver = response.request.meta["driver"]
#
#         if element_exists(driver, By.CSS_SELECTOR, "button.btn:nth-child(5)"):
#             driver.execute_script(
#                 "document.getElementsByClassName('btn primary')[0].click()"
#             )
#         time.sleep(3)
#         self.logger.warning("DRIVER URL !!!!!!!!!!!!!!!!!!!!!!")
#         self.logger.warning(str(driver.current_url))
#         if element_exists(
#             driver,
#             By.XPATH,
#             "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/button",
#         ):
#             driver.find_element(
#                 by=By.XPATH,
#                 value="/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/button",
#             ).click()
#
#             statement_type = response.meta.get("statement_type")
#             self.logger.warning(
#                 "HERE IS THE STATEMENT TYPE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#             )
#             self.logger.warning(f"{str(response.url)}, {statement_type}")
#             document: DocumentModel = response.meta.get("document")
#             financial_statement = FinancialStatementItem()
#             financial_statement["metadata"] = document.__dict__
#             rows = self.get_rows(driver)
#
#             statement_type = self.fields_processor.extract_statement_type(rows)
#             elements_by_column = self.extract_elements_by_column(rows, statement_type)
#
#             local_statement_type = self.local_statement_types[statement_type]
#             financial_statement["metadata"].update(
#                 {"statement_type": local_statement_type}
#             )
#             financial_statement["data"] = elements_by_column
#             yield financial_statement
#         else:
#             yield None
#
#     # def get_rows(self, response):
#     #     table = response.xpath("//div[contains(@class, 'D(tbr)')]")
#     #
#     #     parsed_rows = []
#     #
#     #     if table:
#     #         for row in table:
#     #             element = row.xpath("./div")
#     #             parsed_row = []
#     #             for item in element:
#     #                 try:
#     #                     text = item.xpath(".//span/text()[1]").get()
#     #                     if text:
#     #                         parsed_row.append(text)
#     #                     else:
#     #                         parsed_row.append(None)
#     #                 except ValueError:
#     #                     parsed_row.append(None)
#     #             parsed_rows.append(parsed_row)
#     #         return parsed_rows
#
#     def get_rows(self, driver):
#         table = driver.find_elements(
#             by=By.XPATH, value="//div[contains(@class, 'D(tbr)')]"
#         )
#         parsed_rows = []
#         if table:
#             self.logger.warning(
#                 "THERE ARE ITEMS AVAILABLE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#             )
#             for row in table:
#                 elements = row.find_elements(by=By.XPATH, value="./div")
#                 parsed_row = []
#                 for element in elements:
#                     text = element.text
#                     parsed_row.append(text)
#                 parsed_rows.append(parsed_row)
#             return parsed_rows
#
#     def extract_elements_by_column(self, rows: list, statement_type):
#         if rows:
#             self.logger.warning(
#                 "HERE ARE THE ROWS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#             )
#             self.logger.warning(str(rows))
#             container = []
#             for column in range(1, len(rows[0])):
#                 period = rows[0][column]
#                 rows_by_period = {"period": period}
#                 self.logger.warning(str(self.normalized_fields[statement_type]))
#                 for row in rows[1:]:
#                     if row[0] in self.normalized_fields[statement_type]:
#                         local_field = self.normalized_fields[statement_type][row[0]]
#                         rows_by_period.update({local_field: row[column]})
#                 container.append(rows_by_period)
#             self.logger.warning(
#                 "HERE ARE THE TRANSFORMED ROWS!!!!!!!!!!!!!!!!!!!!!!!!!!"
#             )
#             self.logger.warning(str(container))
#             return container
