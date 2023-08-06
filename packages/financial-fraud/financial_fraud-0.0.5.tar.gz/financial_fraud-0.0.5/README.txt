# Financial Fraud Library Describtion:
### This the first financial fraud dedtection python library which includes evelen different of the most crucial financial fraud dedtection scenarios which can be used within any financial institution/group as a financial fraud dedection monitoring engine or included within current monitoring engine setup. 
### It can also be used manually in order to set up monitoring and verification ad-hoc analysis or simulations.

## The Financial Fraud Detection Scenarios:
1. Suspiciously large Transactions Scenario: The large_transactions function is dedicated to detect any cash fraudulent patterns. we needed a function to that catches any unusually large cash transactions made by an individual or company by comparing each transaction amount with the customer type’s threshold we are able to detect any increase in cash. Another advantage for this function is monitoring above the threshold transactions, both deposits and withdrawals.

The large_transactions function takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, transaction identifications, customer type, transaction type, recipient country, transaction amount, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
large_txns = financial_fraud.large_transactions(df, df_threshold, datestamp)

```

2. Suspiciously large Transactions Scenario: The frequent_transactions function is dedicated to detect frequent fraudulent patterns. we needed a function that monitors numerous credit and deposit slips so that the total of each slip is unremarkable, but the total of all the amount is significant. The function checks the frequency of each customer grouped transactions and compare it with the customer type threshold. Additionally, we are able to monitor any substantial increases each customers transaction frequency which might detect an increase in each customer volumes.

The frequent_transactions function takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, transaction identifications, customer type, transaction type, recipient country, transaction amount, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
frequent_txns = financial_fraud.frequent_transactions(df, df_threshold, datestamp)

```
3. High Risk Transactions Scenario: The high_risk function is dedicated to detect any transaction connect to the high risk jurisdictions and tax heavens. The great addition in this function is that the user passes their own high risk data-set with the high risk and tax heaven jurisdictions. since high risk and tax heaven list change ever so often, so having the list being dynamically ingested to the function is a great addition as it allow users more functionality and freedom.

The highfunction takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, transaction identifications, customer type, transaction type, recipient country, transaction amount, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, country.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
high_risk = financial_fraud.high_risk(df, df_threshold, datestamp)

```
4. The Dormant Accounts Scenario: The dormant_customers function is created to large transactions initiated from a previously dormant/inactive customers for a specific timestamp. How the function is detecting such pattern is that firs the function calculates the transactions within the time constraint
the user is specified then it sorts the transactions based on the timestamp, then group the transactions for each customer and get a data-set of customer identifications and timestamp for all the customer that have above the threshold transactions with at least 6 months apart.

The dormant_customers function takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, transaction identifications, customer type, transaction type, recipient country, transaction amount, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
dormant_accounts = financial_fraud_.dormant_accounts(self, df, datestamp)

```
5. The Monthly Smurfing Scenario: The monthly_smurfing function is the monthly_sumrfing function which is dedicated to monitor frequent slips, below a certain threshold amount so that at the end of each month they sum up into a significant amount of money. such customer pattern often go undetected because the frequent slips are very small (based on each customer type of course) that it end up not being monitored in the first place. The function, monitors all cash transactions that are just below the minimum threshold then run the output on each customer type monthly count threshold. This way we ensured that even the smallest transactions are being detected and taken into consideration.

The monthly_smurfing function takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, transaction identifications, customer type, transaction type, recipient country, transaction amount, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
monthly_smurf = financial_fraud_.monthly_smurfing(df, df_threshold, datestamp, min_amount)

```

6. The Deposit Repository Scenario: The deposit_repository function is dedicated for detecting customer patterns that involves accounts used as a deposit repository for funds. In such patterns the customer deposit money from one account to another and this is usually done over a number of transaction slips so the customers refrain from sending large customers but usually opt for frequent ones. this is why for this function after filtering all the transactions within the specified timestamp and the deposits we group the data based on the customer identifications and type then return all the above the threshold data.

The deposit_repository function takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, account identifications, recipient customer identifications, recipient account identifications, transaction identifications, customer type, transaction type, transaction amount, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
deposit_repo = financial_fraud_.mdeposit_repository(df, df_threshold, datestamp)

```
7. The cash_repository function is similar to the above function however here we are detecting repository accounts for cash funds rather than deposits. the previous function monitors all kind of deposit transactions, here we are only interested in cash transactions and they present a higher risk for specific customer groups.

The cash_repository function takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, account identifications, recipient customer identifications, recipient account identifications, transaction identifications, customer type, transaction type, transaction amount, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
cash_repo = financial_fraud_.cash_repository(df, df_threshold, datestamp)

```

8. The Large Exchange Scenario: The large_exchange function is responsible for detecting suspicious patterns when customers perform large exchange transactions. exchange transactions are when the customer exchange one currency into another different currency. this function filters out all exchange transactions for the specified time constraint and only keeps transactions that are higher than or equal to the specified threshold for each customer type.

The large_exchange function takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, account identifications, recipient customer identifications, recipient account identifications, transaction identifications, customer type, transaction type, transaction amount, sender currency, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
large_exchange = financial_fraud_.large_exchange(df, df_threshold, datestamp)

```

9. The Frequent Exchange Scenario: The frequent_exchange function is similar to the large_exchange function, the only differ-
ence is that instead of detecting large transactions we are detecting frequent transactions. Meaning that we are grouping the transaction count for each customer and customer type, then we are comparing these counts with the threshold data-set customer type threshold.

The frequent_exchange function takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, account identifications, recipient customer identifications, recipient account identifications, transaction identifications, customer type, transaction type, transaction amount, sender currency, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
frequent_exchange = financial_fraud_.frequent_exchange(df, df_threshold, datestamp)

```

10. The Large Overseas Scenario: The large_overseas function is one of the important and crucial function in any transaction monitoring engine because this function detect all the large above the specified threshold for each customer type transactions. A point worth mentioning here is that overseas transactions are very different from high risk and tax heaven transactions which means that overseas transaction are defined as transactions where the transaction country of initiation is different from the destination country. This also doesn’t mean that it has to be necessarily the customer country of origin, rather than simply being the country where this transaction was issued from.

The large_overseas function takes the following three arguments:

    1. transactions data-frame: the transactions data-set should have the following data attributes in this specific order: customer identifications, transaction identifications, customer type, transaction type, recipient country, transaction amount, timestamp.

    2. country data-frame: the country data-set contains the following data attributes: customer type, country.

    3. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    4. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
large_overseas_ = financial_fraud_.large_overseas(df, df_country, df_threshold, datestamp)

```

11. The Balance Overseas Scenario: The balance_overseas function is an interesting function because here we detect the pattern where a user starts to build up balances overseas. this is particularly tricky because different countries have different controls in regards of AML/CTF. furthermore, different financial institutions have different controls. so a suspicious activity in your institutions doesn’t necessarily means it’s being handled as such on the recipient side.

The balance_overseas function takes the following three arguments:

    1. transactions data-frame: customer identifications, account identifications, recipient customer identifications, recipient account identifications, transaction identifications, customer type, transaction type, transaction amount, sender country, recipient country, timestamp.

    2. threshold data-frame: the threshold data-set should have the following data attributes in this specific order: customer type, threshold.

    3. time constrain: here we specify the number of months we want the function to look back at.

```
financial_fraud_ = financial_fraud()
balance_overseas_ = financial_fraud_.balance_overseas(df, df_threshold, datestamp)

```