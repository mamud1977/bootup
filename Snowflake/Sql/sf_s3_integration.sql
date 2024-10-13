-- What do we learn here?
-- 1. integration object
-- 2. Trust relationship with AWS S3
-- 3. File format 
-- 4. Load csv/json file from AWS S3
-- 5. JSON flattening



USE SRC_DB.SCOTT;

-- Creating integration object

CREATE OR REPLACE STORAGE INTEGRATION s3_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::682033475666:role/role-for-snowflake-users'
  STORAGE_ALLOWED_LOCATIONS = ('s3://data-for-all-work/')
  --STORAGE_BLOCKED_LOCATIONS = ('s3://mybucket1/mypath1/sensitivedata/', 's3://mybucket2/mypath2/sensitivedata/')
  ;

DESC INTEGRATION s3_int;

-- Record the following values for trust relationship 
STORAGE_AWS_IAM_USER_ARN = arn:aws:iam::442042540193:user/kfcr0000-s
STORAGE_AWS_ROLE_ARN = arn:aws:iam::682033475666:role/role-for-snowflake-users
STORAGE_AWS_EXTERNAL_ID = RYB43760_SFCRole=4_qFGJm/z7cxm9VnxHXonw4LR/mi0=


CREATE OR REPLACE STAGE my_s3_stage
    URL = 's3://data-for-all-work/'
    STORAGE_INTEGRATION = s3_int
  --  FILE_FORMAT = my_csv

-- upload some files

list @my_s3_stage

Create or replace table rainfall 
(
num number(38,0),
altitude number(38,0),
sep number(38,1),
oct number(38,1),
nov number(38,1),
dec number(38,1),
jan number(38,1),
feb number(38,1),
mar number(38,1),
apr number(38,1),
may number(38,1),
name  varchar(256),
x_utm number(38,4),
y_utm number(38,4)
)


CREATE OR REPLACE FILE FORMAT my_csv 
  TYPE = 'CSV' 
  FIELD_DELIMITER = ',' 
  RECORD_DELIMITER = '\n' 
  SKIP_HEADER = 1
  EMPTY_FIELD_AS_NULL = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '\"';


SHOW FILE FORMATS;


COPY INTO rainfall from @my_s3_stage/csv/rainfall.csv
file_format = (format_name = my_csv);


select * from rainfall 



-- ++++++++++++++++++++++++++++++++++++++++++++++
--  JSON handling 
-- ++++++++++++++++++++++++++++++++++++++++++++++

CREATE OR REPLACE FILE FORMAT my_json 
  TYPE = 'JSON'
  STRIP_OUTER_ARRAY = TRUE; 

list @my_s3_stage/json
  
CREATE OR REPLACE TABLE mytable_json (
  JSON_DATA VARIANT
);


COPY INTO mytable_json
FROM @my_s3_stage/json/example_2.json
FILE_FORMAT = (format_name = my_json );

select * from mytable_json

SELECT
JSON_DATA:"color",
JSON_DATA:"quiz":"maths"
FROM mytable_json

SELECT 
    *
FROM mytable_json
,LATERAL FLATTEN (input => JSON_DATA:quiz);


