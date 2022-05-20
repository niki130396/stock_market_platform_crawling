CREATE TABLE IF NOT EXISTS crawling_financialstatementline (
    field_id integer PRIMARY KEY,
    name varchar(155),
    description varchar(255),
    crawling_source_id integer,
    normalized_field_id integer,
    statement_type_id integer,
    FOREIGN KEY (crawling_source_id) REFERENCES crawling_crawlingsourcedetails (crawling_source_id),
    FOREIGN KEY (normalized_field_id) REFERENCES crawling_normalizedfieldtree (field_id),
    FOREIGN KEY (statement_type_id) REFERENCES crawling_statementtypelocaldefinition (statement_type_definition_id)
);
