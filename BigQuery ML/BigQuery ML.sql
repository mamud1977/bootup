SELECT
count(*)
FROM `concise-option-423004-a3.equity_transaction.insider_trading`;

SELECT
SYMBOL,
COMPANY,
NAME_OF_ACQUIRER_DISPOSER,
CATEGORY_OF_PERSON,
QTY_OF_SECURITIES_ACQUIRED_DISPLOSED,
TRANSACTION_TYPE,
TRANSACTION_DATE,
MODE_OF_ACQUISITION
FROM `concise-option-423004-a3.equity_transaction.insider_trading`;

SELECT
COMPANY,NAME_OF_ACQUIRER_DISPOSER,TRANSACTION_TYPE
FROM `concise-option-423004-a3.equity_transaction.insider_trading`;

CREATE OR REPLACE MODEL 
  `concise-option-423004-a3.equity_transaction.trading_patterm`
OPTIONS
(
model_type = 'LOGISTIC_REG',
auto_class_weights = TRUE,
data_split_method = 'NO_SPLIT',
input_label_cols = ['TRANSACTION_TYPE'],
max_iteration = 10
)
AS
SELECT
COMPANY,NAME_OF_ACQUIRER_DISPOSER,TRANSACTION_TYPE
FROM `concise-option-423004-a3.equity_transaction.insider_trading`;

SELECT * from ML.EVALUATE
(
  MODEL `concise-option-423004-a3.equity_transaction.trading_patterm`, 
  (
    SELECT
      COMPANY,NAME_OF_ACQUIRER_DISPOSER,TRANSACTION_TYPE
    FROM `concise-option-423004-a3.equity_transaction.insider_trading`
  )
  
)


SELECT * from ML.PREDICT
(
  MODEL `concise-option-423004-a3.equity_transaction.trading_patterm`, 
  (
    SELECT
      'Pidilite Industries Limited' as COMPANY,
      'Neerav Parekh' as NAME_OF_ACQUIRER_DISPOSER
  )
  
)


