Create Database if not exists Retail_demo;

CREATE SCHEMA IF NOT EXISTS Retail_demo.bronze;
CREATE SCHEMA IF NOT EXISTS Retail_demo.SILVER;
CREATE SCHEMA IF NOT EXISTS RETAIL_DEMO.GOLD;
CREATE STAGE IF NOT EXISTS bronze.RAW_FILES;

/*
Read in from Files stage into raw
*/
create or replace TABLE Silver.ITEM_CATEGORY (
	CATEGORY VARCHAR(16777216),
	SUBCATEGORY VARCHAR(16777216),
	ITEM_NAME VARCHAR(16777216),
	BRAND VARCHAR(16777216),
	PRICE NUMBER(38,2),
	CATEGORY_ID NUMBER(38,0),
	SUBCATEGORY_ID NUMBER(38,0),
	ITEM_ID NUMBER(38,0)
);


create or replace TABLE Silver.STORE_MASTER (
	STORE_ID VARCHAR(16777216),
	PROVINCE VARCHAR(16777216),
	CITY VARCHAR(16777216),
	SUBURB VARCHAR(16777216),
	POSTAL_CODE NUMBER(38,0)
);

create or replace TABLE Bronze.Raw_Transactions (
	TRANSACTION_ID VARCHAR(16777216),
	"DATE" DATE,
	STORE_ID VARCHAR(16777216),
	ITEM_ID NUMBER(38,0),
	QUANTITY NUMBER(38,0),
	UNIT_PRICE NUMBER(38,2),
	TOTAL_AMOUNT NUMBER(38,14)
)COMMENT='A table containing synthetic transactions of all stores at item level.'
; 

COPY INTO Retail_demo.Silver.store_master  FROM @Retail_demo.Bronze.RAW_FILES FILES=('StoreMaster.csv') FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1);
COPY INTO Retail_demo.Silver.ITEM_CATEGORY FROM @Retail_demo.Bronze.RAW_FILES FILES=('Item Category.csv') FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1);
COPY INTO Retail_demo.Bronze.Raw_Transactions FROM @Retail_demo.Bronze.RAW_FILES FILES=('2020_2025_Jan.csv') FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1);

/*
SILVER TABLES
*/
/*
Create Base tables
*/

Create or REPLACE TABLE Silver.Aggregated_transactions as (
SELECT 
    "DATE", 
    STORE_ID, 
    ITEM_ID, 
    SUM(Quantity) as Total_Units_Sold, 
    ROUND(SUM(TOTAL_AMOUNT),2) as Total_Amount
from BRONZE.Raw_Transactions group by ("DATE", STORE_ID, ITEM_ID));

Create or replace TABLE Silver.DAILY_STORE_REVENUE as (
SELECT 
    "DATE", 
    STORE_ID, 
    ROUND(SUM(TOTAL_AMOUNT),2) as Total_Amount
from BRONZE.Raw_Transactions group by ("DATE", STORE_ID));

Create or replace TABLE Silver.Daily_Revenue as (
SELECT 
    "DATE", 
    ROUND(SUM(TOTAL_AMOUNT),2) as Total_Amount
from BRONZE.Raw_Transactions group by "DATE");

/* create date time feature table */
CREATE OR REPLACE TABLE Retail_demo.Silver.Date_features AS
SELECT 
    DATEADD(DAY, SEQ4(), '2020-01-01') AS DATE_,
    dayofmonth(DATE_) AS day_of_month,
    DAYOFWEEK(DATE_) AS day_of_week,
    MONTH(DATE_) as month_number,
    weekofyear(DATE_) as week_of_year,
    quarter(DATE_) as quarter_number,
    Year(Date_) as Year_number,
    CASE
        WHEN DAY_OF_WEEK = 6 THEN 1 -- Saturday
        WHEN DAY_OF_WEEK = 0 THEN 1 -- Sunday 
        ELSE 0
    END AS IS_WEEKEND,
    CASE 
        WHEN DATE_ = LAST_DAY(DATE_) THEN 1 
        ELSE 0 
    END AS is_last_day
FROM 
    TABLE(GENERATOR(ROWCOUNT => 2192));
select * from silver.date_features;

/* Create tables to store forecasts */

Create or replace TABLE Gold.XGB_Forecasted_Daily_Revenue (
    "DATE" DATE, 
    PREDICTED_AMOUINT NUMBER);
    
