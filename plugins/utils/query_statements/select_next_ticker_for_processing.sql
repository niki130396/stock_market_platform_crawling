UPDATE "public".financial_statements_statementsmetadata meta
SET is_processed = true,
    is_attempted = true
FROM (SELECT s.*,
             CASE
                WHEN s.is_attempted = false THEN 0
                ELSE 1
             END AS numeric_is_attempted
      FROM (
        SELECT * FROM
            (SELECT * FROM "public".financial_statements_statementsmetadata renew_statements
                WHERE renew_statements.latest_statement_date IS NULL
                OR CURRENT_DATE - renew_statements.latest_statement_date > 90) sub_meta
        WHERE sub_meta.is_available = false
        AND sub_meta.is_processed = false
        ) s
      ORDER BY numeric_is_attempted, symbol
      LIMIT 1) AS subquery
WHERE meta.symbol = subquery.symbol
RETURNING meta.*;
