CREATE TABLE IF NOT EXISTS financial_statements_statementsmetadata (
    company_id integer PRIMARY KEY,
    symbol varchar(10),
    name varchar(100),
    market_cap bigint,
    country varchar(50),
    ipo_year integer,
    volume integer,
    sector varchar(50),
    industry varchar(50),
    is_available boolean,
    is_balance_sheet_statement_available boolean,
    is_cash_flow_statement_available boolean,
    is_income_statement_available boolean,
    is_processed boolean,
    is_attempted boolean,
    latest_statement_date date
);
