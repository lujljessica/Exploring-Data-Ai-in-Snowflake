-- Create the stream to monitor the stage
CREATE STREAM IF NOT EXISTS ingest_transactions_stream ON STAGE bronze.raw_files;

CREATE OR REPLACE TASK ingestion_task
  WAREHOUSE = your_warehouse
  SCHEDULE = 'USING CRON 0 0 * * * UTC'  -- Runs daily at midnight UTC
  WHEN SYSTEM$STREAM_HAS_DATA('ingest_transactions_stream')
AS
  INSERT INTO bronze.transactions (
    transaction_id,
    transaction_date,
    store_id,
    item_id,
    quantity,
    unit_price,
    total_amount,
    source_file,
    load_timestamp
  )
  SELECT 
    $1:"Transaction_ID"::STRING AS transaction_id,
    $1:"Transaction_Date"::TIMESTAMP AS transaction_date,
    $1:"Store_ID"::STRING AS store_id,
    $1:"Item_ID"::STRING AS item_id,
    $1:"Quantity"::INTEGER AS quantity,
    $1:"Unit_Price"::DECIMAL(10,2) AS unit_price,
    $1:"Total_Amount"::DECIMAL(10,2) AS total_amount,
    METADATA$FILENAME AS source_file,
    CURRENT_TIMESTAMP() AS load_timestamp
  FROM ingest_transactions_stream;

-- Activate the task
ALTER TASK ingestion_task RESUME;