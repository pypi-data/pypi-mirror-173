import numpy as np
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

class financial_fraud:
    def large_transactions(self, df, df_threshold, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "transaction_id", "customer_type", "transaction_type", "counter_country", "transaction_amount", "timestamp"]
        df_threshold.columns = ["segment", "threshold"]
        df.customer_id = df.customer_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df.counter_country = df.counter_country.str.strip()
        df_threshold.segment = df_threshold.segment.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.threshold = df_threshold.threshold.astype(float)
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[[todays_date < i for i in df.timestamp.tolist()]].reset_index(drop = True)
        df_cash = df[['credit'.lower() in df.transaction_type[i].lower() for i in range(len(df))]].reset_index(drop= True)
        df["threshold"] = [df_threshold[df_threshold.segment == df.customer_type[i]].threshold.values[0] for i in range(len(df))]
        df_final = df[[df.transaction_amount[i] > df.threshold[i] for i in range(len(df))]].reset_index(drop = True)
        return df_final

    def frequent_transactions(self, df, df_threshold, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "transaction_id", "customer_type", "transaction_type", "counter_country", "transaction_amount", "timestamp"]
        df_threshold.columns = ["segment", "threshold"]
        df.customer_id = df.customer_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df.counter_country = df.counter_country.str.strip()
        df_threshold.segment = df_threshold.segment.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.threshold = df_threshold.threshold.astype(float)
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[[todays_date < i for i in df.timestamp.tolist()]].reset_index(drop = True)
        grouped_data = df.groupby(['customerid', 'customer_type'])['customerid'].count().keys().tolist()
        counted_values = df.groupby(['customerid', 'customer_type'])['customerid'].count().tolist()
        df_final = pd.DataFrame(grouped_data, columns = ['customer_id', 'segment'])
        df_final['counts'] = counted_values
        df_final['threshold'] = [df_threshold[df_threshold.segment == i].threshold.values[0] for i in df_final.segment]
        df_final = df_final[df_final.counts >= df_final.threshold].reset_index(drop = True)
        return df_final
    
    def high_risk(self, df, df_threshold, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "transaction_id", "customer_type", "transaction_type", "counter_country", "transaction_amount", "timestamp"]
        df_threshold.columns = ["segment", "country"]
        df.customer_id = df.customer_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df.counter_country = df.counter_country.str.strip()
        df_threshold.segment = df_threshold.segment.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.country = df_threshold.country.str.strip()
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[[todays_date < i for i in df.timestamp.tolist()]].reset_index(drop = True)
        country_list = df_threshold.country.unique().tolist()
        df = df[[i not in country_list for i in df.counter_country]].reset_index(drop = True)
        return df
    
    def dormant_accounts(self, df, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "transaction_id", "customer_type", "transaction_type", "counter_country", "transaction_amount", "timestamp"]
        df.customer_id = df.customer_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df.counter_country = df.counter_country.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        month_away = datetime.date.today() - relativedelta(months=datestamp)
        calc_days = abs((month_away - datetime.date.today()).days)
        days_ = df.sort_values(['timestamp']).groupby('customer_id')['timestamp'].diff().dt.days
        df = df[days_>=180].reset_index(drop = True)
        return df
    
    def monthly_smurfing(self, df, df_threshold, datestamp, min_amount):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "transaction_id", "customer_type", "transaction_type", "counter_country", "transaction_amount", "timestamp"]
        df_threshold.columns = ["segment", "threshold"]
        df.customer_id = df.customer_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df.counter_country = df.counter_country.str.strip()
        df_threshold.segment = df_threshold.segment.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.threshold = df_threshold.threshold.astype(float)
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[([todays_date < i for i in df.timestamp.tolist()]) & (df.transaction_amount >= min_amount)].reset_index(drop = True)
        df_cash = df[['CRedit'.lower() in df.transaction_type[i].lower() for i in range(len(df))]].reset_index(drop= True)
        df["threshold"] = [df_threshold[df_threshold.segment == df.customer_type[i]].threshold.values[0] for i in range(len(df))]
        df_final = df[[df.transaction_amount[i] > df.threshold[i] for i in range(len(df))]].reset_index(drop = True)
        return df_final
    
    def deposit_repository(self, df, df_threshold, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "account_id", "recipient_customer_id", "recipient_account_id", "transaction_id", "customer_type", "transaction_type", "transaction_amount", "timestamp"]
        df_threshold.columns = ["segment", "threshold"]
        df.customer_id = df.customer_id.str.strip()
        df.account_id = df.account_id.str.strip()
        df.recipient_customer_id = df.recipient_customer_id.str.strip()
        df.recipient_account_id = df.recipient_account_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df_threshold.segment = df_threshold.segment.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.threshold = df_threshold.threshold.astype(float)
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[[todays_date < i for i in df.timestamp.tolist()]].reset_index(drop = True)
        deposit = df[['Deposit'.lower() in df.transaction_type[i].lower() for i in range(len(df))]].reset_index(drop= True)
        df_cleaned = deposit[(deposit.customer_id == deposit.recipient_customer_id) & (deposit.account_id != deposit.recipient_account_id)].reset_index(drop = True)
        df_grouped = df_cleaned.groupby(['customer_id', 'customer_type']).sum('transaction_amount')
        custs_ = [df_grouped.index[i][0] for i in range(len(df_grouped))] 
        segm_ = [df_grouped.index[i][1] for i in range(len(df_grouped))]
        values_ = df_grouped['transaction_amount'].tolist()
        final_df = pd.DataFrame(list(zip(custs_, segm_, values_)), columns = ['customer_id', 'customer_type', 'deposit_amounts'])
        final_df['threshold'] = [df_threshold[df_threshold.segment == final_df.customer_type[i]].threshold.values[0] for i in range(len(final_df))]
        final_df = final_df[final_df['deposit_amounts'] > final_df.threshold].reset_index(drop = True)
        return final_df
    
    def cash_repository(self, df, df_threshold, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "account_id", "recipient_customer_id", "recipient_account_id", "transaction_id", "customer_type", "transaction_type", "transaction_amount", "timestamp"]
        df_threshold.columns = ["segment", "threshold"]
        df.customer_id = df.customer_id.str.strip()
        df.account_id = df.account_id.str.strip()
        df.recipient_customer_id = df.recipient_customer_id.str.strip()
        df.recipient_account_id = df.recipient_account_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df_threshold.segment = df_threshold.segment.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.threshold = df_threshold.threshold.astype(float)
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[[todays_date < i for i in df.timestamp.tolist()]].reset_index(drop = True)
        deposit = df[['Cash'.lower() in df.transaction_type[i].lower() for i in range(len(df))]].reset_index(drop= True)
        df_cleaned = deposit[(deposit.customer_id == deposit.recipient_customer_id) & (deposit.account_id != deposit.recipient_account_id)].reset_index(drop = True)
        df_grouped = df_cleaned.groupby(['customer_id', 'customer_type']).sum('transaction_amount')
        custs_ = [df_grouped.index[i][0] for i in range(len(df_grouped))] 
        segm_ = [df_grouped.index[i][1] for i in range(len(df_grouped))]
        values_ = df_grouped['transaction_amount'].tolist()
        final_df = pd.DataFrame(list(zip(custs_, segm_, values_)), columns = ['customer_id', 'customer_type', 'deposit_amounts'])
        final_df['threshold'] = [df_threshold[df_threshold.segment == final_df.customer_type[i]].threshold.values[0] for i in range(len(final_df))]
        final_df = final_df[final_df['deposit_amounts'] > final_df.threshold].reset_index(drop = True)
        return final_df
    
    def large_exchange(self, df, df_threshold, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "account_id", "recipient_customer_id", "recipient_account_id", "transaction_id", "customer_type", "transaction_type", "transaction_amount", "transaction_currency", "timestamp"]
        df_threshold.columns = ["segment", "threshold"]
        df.customer_id = df.customer_id.str.strip()
        df.account_id = df.account_id.str.strip()
        df.recipient_customer_id = df.recipient_customer_id.str.strip()
        df.recipient_account_id = df.recipient_account_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df.transaction_currency = df.transaction_currency.str.strip()
        df_threshold.segment = df_threshold.segment.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.threshold = df_threshold.threshold.astype(float)
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[[todays_date < i for i in df.timestamp.tolist()]].reset_index(drop = True)
        df["threshold"] = [df_threshold[df_threshold.segment == df.customer_type[i]].threshold.values[0] for i in range(len(df))]
        df = df[[df.transaction_amount[i] > df.threshold[i] for i in range(len(df))]].reset_index(drop = True)
        df_deposit = df[['Deposit'.lower() in df.transaction_type[i].lower() for i in range(len(df))]].reset_index(drop= True)
        df_withdrawal = df[['Withdrawal'.lower() in df.transaction_type[i].lower() for i in range(len(df))]].reset_index(drop= True)
        deposit_list = []
        withdrawal_list = []
        for i in range(len(df_withdrawal)):
            for j in range(len(df_deposit)):
                if(df_withdrawal.customer_id[i] == df_deposit.customer_id[j] and df_withdrawal.transaction_currency[i] != df_deposit.transaction_currency[j] and df_withdrawal.timestamp[i] >= df_deposit.timestamp[j]):
                    withdrawal_list.append(i)
                    deposit_list.append(j)

        deposit_final = df_deposit.iloc[deposit_list]
        withdrawal_final = df_withdrawal.iloc[withdrawal_list]
        final_df = pd.concat([deposit_final,withdrawal_final]).reset_index(drop = True)
        return final_df 
    
    def frequent_exchange(self, df, df_threshold, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "account_id", "recipient_customer_id", "recipient_account_id", "transaction_id", "customer_type", "transaction_type", "transaction_amount", "transaction_currency", "timestamp"]
        df_threshold.columns = ["segment", "threshold"]
        df.customer_id = df.customer_id.str.strip()
        df.account_id = df.account_id.str.strip()
        df.recipient_customer_id = df.recipient_customer_id.str.strip()
        df.recipient_account_id = df.recipient_account_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df.transaction_currency = df.transaction_currency.str.strip()
        df_threshold.segment = df_threshold.segment.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.threshold = df_threshold.threshold.astype(float)
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[[todays_date < i for i in df.timestamp.tolist()]].reset_index(drop = True)
        df["threshold"] = [df_threshold[df_threshold.segment == df.customer_type[i]].threshold.values[0] for i in range(len(df))]
        df_deposit = df[['Deposit'.lower() in df.transaction_type[i].lower() for i in range(len(df))]].reset_index(drop= True)
        df_withdrawal = df[['Withdrawal'.lower() in df.transaction_type[i].lower() for i in range(len(df))]].reset_index(drop= True)
        deposit_list = []
        withdrawal_list = []
        for i in range(len(df_withdrawal)):
            for j in range(len(df_deposit)):
                if(df_withdrawal.customer_id[i] == df_deposit.customer_id[j] and df_withdrawal.transaction_currency[i] != df_deposit.transaction_currency[j] and df_withdrawal.timestamp[i] >= df_deposit.timestamp[j]):
                    withdrawal_list.append(i)
                    deposit_list.append(j)

        deposit_final = df_deposit.iloc[deposit_list]
        withdrawal_final = df_withdrawal.iloc[withdrawal_list]
        concat_df = pd.concat([deposit_final,withdrawal_final]).reset_index(drop = True)
        grouped_data = concat_df.groupby(['customer_id', 'customer_type'])['customer_id'].count().keys().tolist()
        counted_values = concat_df.groupby(['customer_id', 'customer_type'])['customer_id'].count().tolist()
        df_final = pd.DataFrame(grouped_data, columns = ['customer_id', 'segment'])
        df_final['counts'] = counted_values
        df_final['threshold'] = [df_threshold[df_threshold.segment == i].threshold.values[0] for i in df_final.segment]
        df_final = df_final[df_final.counts >= df_final.threshold].reset_index(drop = True)
        return df_final
    
    def large_overseas(self, df, df_country, df_threshold, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "transaction_id", "customer_type", "transaction_type", "counter_country", "transaction_amount", "timestamp"]
        df_country.columns = ["segment", "country"]
        df_threshold.columns = ["segment", "threshold"]
        df.customer_id = df.customer_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df.counter_country = df.counter_country.str.strip()
        df_country.segment = df_country.segment.str.strip()
        df_country.country = df_country.country.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.segment = df_threshold.segment.str.strip()
        df_threshold.threshold = df_threshold.threshold.astype(float)
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[[todays_date < i for i in df.timestamp.tolist()]].reset_index(drop = True)
        country_list = df_country.country.unique().tolist()
        df = df[[i not in country_list for i in df.counter_country]].reset_index(drop = True)
        df["threshold"] = [df_threshold[df_threshold.segment == df.customer_type[i]].threshold.values[0] for i in range(len(df))]
        df_final = df[[df.transaction_amount[i] > df.threshold[i] for i in range(len(df))]].reset_index(drop = True)
        return df_final
    
    def balance_overseas(self, df, df_threshold, datestamp):
        df = df.dropna().reset_index(drop = True)
        df.columns = ["customer_id", "account_id", "recipient_customer_id", "recipient_account_id", "transaction_id", "customer_type", "transaction_type", "transaction_amount", "sender_country", "counter_country", "timestamp"]
        df_threshold.columns = ["segment", "threshold"]
        df.customer_id = df.customer_id.str.strip()
        df.account_id = df.account_id.str.strip()
        df.recipient_customer_id = df.recipient_customer_id.str.strip()
        df.recipient_account_id = df.recipient_account_id.str.strip()
        df.transaction_id = df.transaction_id.str.strip()
        df.customer_type = df.customer_type.str.strip()
        df.transaction_type = df.transaction_type.str.strip()
        df.sender_country = df.sender_country.str.strip()
        df.counter_country = df.counter_country.str.strip()
        df_threshold.segment = df_threshold.segment.str.strip()
        df.transaction_amount = df.transaction_amount.astype(float)
        df_threshold.threshold = df_threshold.threshold.astype(float)
        todays_date = datetime.date.today() + relativedelta(months=-datestamp)
        df = df[[todays_date < i for i in df.timestamp.tolist()]].reset_index(drop = True)
        df = df[df.sender_country != df.counter_country].reset_index(drop = True)
        df["threshold"] = [df_threshold[df_threshold.segment == df.customer_type[i]].threshold.values[0] for i in range(len(df))]
        df_final = df[[df.transaction_amount[i] > df.threshold[i] for i in range(len(df))]].reset_index(drop = True)
        return df_final

