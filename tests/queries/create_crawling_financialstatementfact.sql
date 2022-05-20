CREATE TABLE IF NOT EXISTS crawling_financialstatementfact (
    fact_id integer PRIMARY KEY,
    fiscal_period date,
    unit varchar(50),
    value integer,
    company_id integer,
    financial_statement_line_id integer,
    FOREIGN KEY(company_id) REFERENCES financial_statements_statementsmetadata(company_id),
    FOREIGN KEY(financial_statement_line_id) REFERENCES crawling_financialstatementline(field_id)
);