CREATE OR REPLACE PROCEDURE create_training_set(tbl_name VARCHAR, date_col VARCHAR)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    training_view_name STRING DEFAULT  'VW_' || tbl_name||  '_TRAIN';
    sql_stmt STRING;
BEGIN
    sql_stmt := '
    CREATE OR REPLACE VIEW ' || training_view_name || ' AS (
        WITH ordered_revenue AS (
            SELECT  
                *,
                ROW_NUMBER() OVER (ORDER BY ' || date_col || ') AS row_num
            FROM
                ' || tbl_name || '
        ), 
        total_rows AS (
            SELECT
                COUNT(*) AS total_count
            FROM
                ' || tbl_name || '
        )
        SELECT 
            * EXCLUDE (row_num)
        FROM
            ordered_revenue
        WHERE
            row_num <= (SELECT total_count * 0.8 FROM total_rows)
        ORDER BY
            ' || date_col || '
    );';
    EXECUTE IMMEDIATE sql_stmt;

    -- Return a success message
    RETURN 'Training view : ' || training_view_name || ' created successfully.';
END;
$$;

CREATE OR REPLACE PROCEDURE create_test_set(tbl_name VARCHAR, date_col VARCHAR)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    training_view_name STRING DEFAULT  'VW_' || tbl_name||  '_TRAIN';
    test_view_name STRING DEFAULT  'VW_' || tbl_name||  '_TEST';
    sql_stmt STRING;
BEGIN
    sql_stmt := '
    CREATE OR REPLACE VIEW ' || test_view_name || ' AS (
        SELECT d.*
            FROM ' || tbl_name || ' as d
        LEFT JOIN ' || training_view_name || ' as f
            ON d.' || date_col || ' = f.' || date_col || '
        WHERE f.' || date_col || ' IS NULL
        ORDER BY d.' || date_col || '
    );';
    EXECUTE IMMEDIATE sql_stmt;
    RETURN 'Test view : ' || test_view_name || ' created successfully.';
END;
$$ ;

call create_training_set('daily_revenue', 'transaction_date');
call create_test_set('daily_revenue', 'transaction_date');


call create_training_set('aggregated_transactions', 'transaction_date');
call create_test_set('aggregated_transactions', 'transaction_date');

call create_training_set('daily_store_revenue', 'transaction_date');
call create_test_set('daily_store_revenue', 'transaction_date');

