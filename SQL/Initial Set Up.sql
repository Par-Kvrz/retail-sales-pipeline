-- CREATE A WAREHOUSE (EXTRA SMALL, AUTO SUSPEND AFTER 5 MINUTES)
CREATE WAREHOUSE RETAIL_WH 
    WAREHOUSE_SIZE = XSMALL
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

USE WAREHOUSE RETAIL_WH;

CREATE DATABASE RETAIL_PROJECT;

CREATE SCHEMA RETAIL_PROJECT.STAGING;
CREATE SCHEMA RETAIL_PROJECT.CORE;

USE SCHEMA RETAIL_PROJECT.STAGING;

-- USING TRANSIENT SINCE THIS IS A PERSONAL PROJECT AND WE CAN SAVE THE FAILSAFE COST
-- REMOVING SPACES IN COLUMN NAMES COMPARED TO THE ORIGINAL TABLE
CREATE OR REPLACE TRANSIENT TABLE STG_SUPERSTORE_SALES (
    ROW_ID INT,
    ORDER_ID STRING,
    ORDER_DATE DATE,
    SHIP_DATE DATE,
    SHIP_MODE STRING,
    CUSTOMER_ID STRING,
    CUSTOMER_NAME STRING,
    SEGMENT STRING,
    COUNTRY STRING,
    CITY STRING,
    STATE STRING,
    POSTAL_CODE STRING,
    REGION STRING,
    PRODUCT_ID STRING,
    CATEGORY STRING,
    SUB_CATEGORY STRING,
    PRODUCT_NAME STRING,
    SALES FLOAT
);

CREATE OR REPLACE FILE FORMAT CSV_FILEFORMAT
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null')
    EMPTY_FIELD_AS_NULL = TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY = '"';

-- CONNECTING TO AWS S3
CREATE OR REPLACE STORAGE INTEGRATION SUPERSTORE_INT
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = S3
    ENABLED = TRUE
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::327063582168:role/snowflake-access-role'
    STORAGE_ALLOWED_LOCATIONS = ('s3://superstore-sales-project/');

DESC INTEGRATION SUPERSTORE_INT;

-- CREATING THE STAGE
CREATE OR REPLACE STAGE SUPERSTORE_STAGE
    URL = 's3://superstore-sales-project/'
    STORAGE_INTEGRATION = SUPERSTORE_INT
    FILE_FORMAT = CSV_FILEFORMAT;

-- SEEING THE CONTENT OF THE STAGE, I CAN SEE THE CSV IN S3!
LIST @SUPERSTORE_STAGE;

-- THERE IS NO NEED FOR A PIPE SINCE THIS IS ONE-TIME DATA, BUT JUST FOR FUN AND DEMONSTRATION!
-- NO NEED FOR AUTO-INGEST
CREATE OR REPLACE PIPE SUPERSTORE_PIPE AS
    COPY INTO STG_SUPERSTORE_SALES
    FROM @SUPERSTORE_STAGE
    FILE_FORMAT = (FORMAT_NAME = 'CSV_FILEFORMAT')
    ON_ERROR = 'CONTINUE';

ALTER PIPE SUPERSTORE_PIPE REFRESH;

-- MAKING SURE THE DATA IS IN THE TABLE
SELECT * FROM STG_SUPERSTORE_SALES LIMIT 10;
