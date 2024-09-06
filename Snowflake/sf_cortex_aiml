USE ROLE ACCOUNTADMIN;

CREATE WAREHOUSE IF NOT EXISTS DASH_S WAREHOUSE_SIZE=SMALL;
CREATE DATABASE IF NOT EXISTS DASH_DB;
CREATE SCHEMA IF NOT EXISTS DASH_SCHEMA;

USE DASH_DB.DASH_SCHEMA;
USE WAREHOUSE DASH_S;

CREATE OR REPLACE STAGE MY_CORTEX_STG
	DIRECTORY = ( ENABLE = true ) 
	ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' );

CREATE OR REPLACE FILE FORMAT myformat TYPE = 'csv' FIELD_DELIMITER = ',' SKIP_HEADER = 1;

LIST @MY_CORTEX_STG

-- Used this publicly available data: https://www.kaggle.com/datasets/abhi8923shriv/sentiment-analysis-dataset/data
-- Load Test.csv file 

LIST @MY_CORTEX_STG

SELECT $1, $2, $3, $4 FROM @my_cortex_stg/test.csv
 (FILE_FORMAT =>'myformat') a;


Create or replace table Test
(
textID VARCHAR(100),	
text VARCHAR(4000),
sentiment VARCHAR(100),		
Time_of_Tweet VARCHAR(100),		
Age_of_User VARCHAR(100),		
Country VARCHAR(100),		
Population NUMBER(38,0),	
Land_Area_Km2 NUMBER(38,0),	
Density_P_per_Km2 NUMBER(38,0)
)

show grants on stage DASH_DB.DASH_SCHEMA.my_cortex_stg;

COPY INTO Test from @my_cortex_stg/test.csv FILE_FORMAT ='myformat' on_error='continue' 

update DASH_DB.DASH_SCHEMA.Test
set text = 'My experience went very smoothly, and the person I spoke to was incredibly patient, knowledgeable, and clearly dedicated to finding a solution for my problem. However, the last resort he suggested required that I reinstall the OS on my device. Since the process could take up to thirty minutes, he suggested that we set up a call back, just in case my problem was not resolved after the reinstallation is finished. The callback was not really needed because my problem was resolved. When I received the call, I was ready to answer and thank the person I had spoken to earlier. I was surprised to find that I was speaking to an automated machine; I was being told that I had missed my callback and would be called again later. The same thing happened with the second call as well. This did not really affect my experience because my issue was resolved; however, if it were not, I would have been extremely frustrated for not being able to speak to a customer service representative.'
where 
textid = 'aeb0e9d730'


update DASH_DB.DASH_SCHEMA.Test
set text = 'The level 2 manager I dealt with was the "WORST" I have ve ever dealt with.. He was more in tune to letting me know his title about 6 times and after spending an hour on phone with him he told me I had to have a credit card for the new phone being sent. I have a debit card but he told me required to have a credit card.. . Finally after being given bad information to start with from T mobile it was finally rectified after more than 3.5 hours on calls and over 5 hours of traveling and time spent waiting at the Apple store which was a total waste of time.  After hour on calls i was told to go to apple store.  Apple store told me they would not look at the phone because it was a refurbed phone from 3 party .    Huge waste of my only day off Sunday.   Spent ENTIRE day dealing with something that should not have taken 30 mins most..'
where 
textid in ('c672c9da1d')


update DASH_DB.DASH_SCHEMA.Test
set text = 'iTunes/Apple Music on Windows 10 seems to be buggy, i.e. buttons not working, application not closing, playlists instructions appearing after the fact, etc. The call agent fond the situation abnormal but was not knowledgeable.'
where 
textid in ('33987a8ee5')


update DASH_DB.DASH_SCHEMA.Test
set text = 'En el momento de recoger el equipo; realmente tuve que esperar mucho, casi una hora, estaba cansada, porque todo el tiempo está uno de pie. Gracias'
where 
textid in ('6d846d7d50')

select * from Test where textid in ('aeb0e9d730','c672c9da1d', '33987a8ee5', '6d846d7d50')


-- rm @my_cortex_stg/test.csv
-- drop stage if exists my_cortex_stg 

--------------------------------------------------
------- Translate
--------------------------------------------------
select SNOWFLAKE.CORTEX.TRANSLATE('Cliente esperó casi una hora para recoger el equipo, causando cansancio debido a estar de pie todo el tiempo.','es','en') 



select text, SNOWFLAKE.CORTEX.TRANSLATE(text,'es','en') 
from Test 
--where textid in ('aeb0e9d730','c672c9da1d', '33987a8ee5', '6d846d7d50')
limit 100;


--------------------------------------------------
------- Sentiment Score
--------------------------------------------------

select text, sentiment, snowflake.cortex.sentiment(text) as pred_sentiment 
from Test 
where textid in ('aeb0e9d730','c672c9da1d', '33987a8ee5', '6d846d7d50')
limit 100;


--------------------------------------------------
------- Summarize 
--------------------------------------------------

set var = 'The CORTEX_USER database role in the SNOWFLAKE database includes the privileges that allow users to call Snowflake Cortex LLM functions. By default, the CORTEX_USER role is granted to the PUBLIC role.'

show variables

select $var,snowflake.cortex.summarize($var) as summary from Test limit 100;

select text,snowflake.cortex.summarize(text) as summary from Test limit 100;

select text, snowflake.cortex.summarize(text) as summary, len(snowflake.cortex.summarize(text)) as summary_length  
from Test 
--where textid in ('aeb0e9d730','c672c9da1d', '33987a8ee5', '6d846d7d50')  
limit 100;

--------------------------------------------------
------- Summary with token count
--------------------------------------------------

select 
text, 
snowflake.cortex.summarize(text) as summary, 
snowflake.cortex.count_tokens('summarize',text) as number_of_tokens 
from Test 
where textid in ('aeb0e9d730','c672c9da1d', '33987a8ee5', '6d846d7d50')  
limit 100;


select 
snowflake.cortex.summarize(
$$Mercedes-Benz India on Thursday added its most luxurious electric vehicle (EV) — the EQS Maybach 680 —priced upwards of ₹2.5 crore to its portfolio of EVs, which has seen a 5 per cent penetration in its overall sales. With the EQS Maybach, Mercedes will have five EVs in its portfolio comprising the EQA, the EQB, the EQE, the EQS 580 and now the EQS Maybach.$$
) as news 
from dual


select 
snowflake.cortex.summarize($var) as summary, 
snowflake.cortex.count_tokens('summarize',$var) as number_of_tokens 
from Test 
limit 1;


--------------------------------------------------
------- To select the model
------- To do prompt engineering
------- https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions
--------------------------------------------------

SET prompt = 
'### 
Summarize this transcript in less than 100 words. 
Put the product name, defect and summary in Table format. 
###';

select textid, snowflake.cortex.complete('llama3.1-405b',concat('[INST]',$prompt,text,'[/INST]')) as summary
from Test 
where textid in ('aeb0e9d730','c672c9da1d', '33987a8ee5', '6d846d7d50')
limit 100;

-- snowflake-arctic
{
  "product_name": "OS reinstallation",
  "defect": "Automated callback system",
  "summary": "Customer service experience was positive, but automated callback system caused frustration."
}

-- llama3.1-405b
{
  "Product Name": "Not specified",
  "Defect": "Callback system malfunction",
  "Summary": "Customer's issue resolved, but callback system was flawed"
}

-- reka-core ( not supported)
