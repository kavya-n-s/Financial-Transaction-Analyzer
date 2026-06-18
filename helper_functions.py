import pandas as pd
import json 
import config

# Read CSV
def read_csv(path):
    df=pd.read_csv(path)
    return df

# Data cleansing
def data_cleanser(df):
    df['category'] = df['category'].str.strip().str.title()
    df['date'] = pd.to_datetime(df['date'], format= config.DEFAULT_DATE_FORMAT)
    df['month']= df['date'].dt.month_name()
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    return df

# Calculate total spent, average transaction amount, highest transaction, lowest transaction
def summarizer(df,column,func):
    summarized = func(df[column])
    return summarized

# Group sum of spent
def group_by(df, parameter):
    result_df = df.groupby(parameter)['amount'].sum()
    return result_df

# Dump dataframe to CSV
def df_to_csv(df,path):
    df.to_csv(path)

# JSON dump
def json_dump(path,summary):
    with open(path,'w') as fh:
        json.dump(summary,fh,indent=4)
    return "Summary generated to JSON"

# Monthly category rankingl
def mon_cat_rank(df):
    monthly_category = df.groupby(['month','category'])['amount'].sum().reset_index().sort_values(by='amount',ascending=False)
    return monthly_category

# Transactions above threshold
def high_val_txn(threshold,df):
    threshold = int(threshold)
    filtered = df.query('amount>@threshold')
    return filtered

# Payment Method Analysis Pivot
def pivot_analysis(df,parameter):
    pay_methods = df.groupby(parameter)['amount'].sum().reset_index()
    pma= pd.DataFrame()

    pma = df.pivot_table(values='amount', columns=parameter, index='date', aggfunc='sum',fill_value=0)
    # add row wise total to pma
    pma['daily_spent'] = pma.sum(axis=1)
    # add column wise total to pma
    pma.loc['method_spent'] = pma.sum(axis=0)
    return(pma)

# Filter on any one column based on value
def filter_one_level(df,filter_parameter,filter_value):
    filtered = df.query(f"{filter_parameter} == @filter_value")
    return filtered


def data_validation_report_generator(df, report):
    
#  Validation layer 
    null_category = df[df["category"].isna()]
    null_cat_count = null_category.shape[0]

    null_amount = df[df["amount"].isna()]
    null_amount_count = null_amount.shape[0]

    null_status = df[df["status"].isna()]
    null_stat_count = null_status.shape[0]

# Negative Amounts
    negative_amounts= df[df['amount']<0]
    neg_count = negative_amounts.shape[0]

# Validate Incorrrect status
    invalid_status = df[~df['status'].isin(['SUCCESS','PENDING','FAILED'])]
    invalid_status_count = invalid_status.shape[0]

# Validate Incorrect Region
    invalid_region = df[~df['region'].isin(['USA','UAE','India'])]
    invalid_region_count = invalid_region.shape[0]

# Total invalid rows and DQ score
    invalid_mask = (
        df['category'].isna()
        | df['amount'].isna()
        | df['status'].isna()
        | (df['amount']<0)
        | (~df['status'].isin(['SUCCESS','PENDING','FAILED']))
        | (~df['region'].isin(['USA','UAE','India']))
    )
    invalid_df = df[invalid_mask]
    invalid_row_count = invalid_df.shape[0]
    total_row_count = len(df)
    dq_score = ((total_row_count-invalid_row_count)/total_row_count)*100

# Validation summary
    summary_df = pd.DataFrame({
        "Validation" : ['Null Category','Null Amount','Null Status','Negative Amounts','Invalid Status','Invalid Region', 'Total Invalid rows', 'Data Quality score'],
        "Count of affected rows" : [null_cat_count, null_amount_count, null_stat_count, neg_count, invalid_status_count, invalid_region_count, invalid_row_count, dq_score]
    })

    with pd.ExcelWriter(report, engine='openpyxl') as fh:
        summary_df.to_excel(fh, sheet_name='Validation Summary', index=False)
        null_category.to_excel(fh, sheet_name='Null Category', index=False)
        null_amount.to_excel(fh, sheet_name='Null Amount', index=False)
        null_status.to_excel(fh, sheet_name='Null Status', index=False)
        negative_amounts.to_excel(fh, sheet_name='Negative Amounts', index=False)
        invalid_status.to_excel(fh, sheet_name='Invalid Status', index=False)
        invalid_region.to_excel(fh, sheet_name='Invalid Region', index=False)
    
    for index, row in summary_df.iterrows():
        if row["Count of affected rows"]>0 and row["Validation"] != 'Data Quality score':
            print(f"Data validation done for {row["Validation"]}. Check the input data")

        
