import helper_functions
import config
import pandas as pd
import time

# Read CSV
start_time = time.time()
print("Reading dataset..")
path = config.INPUT_FILE
df = helper_functions.read_csv(path)

# Data cleansing
print("Performaing basic cleansing of dataset..")
df = helper_functions.data_cleanser(df)

# Data Validation
print("Performaing data validation..")
helper_functions.data_validation_report_generator(df, config.VALIDATION_REPORT)

# Calculate summary
total_spent = helper_functions.summarizer(df,'amount',sum)
avg_spent = helper_functions.summarizer(df,'amount',pd.Series.mean)
max_spent = helper_functions.summarizer(df,'amount',max)
min_spent = helper_functions.summarizer(df,'amount',min)

# Calculate spent by category
print("Transaction Analysis in progress..")
spent_by_category = helper_functions.group_by(df,'category')
helper_functions.df_to_csv(spent_by_category,config.CAT_CSV)

# Calculate spent by payment method
spent_by_payment = helper_functions.group_by(df,'payment_method')
helper_functions.df_to_csv(spent_by_payment,config.PAY_METH_CSV)

# Calculate spent by region
spent_by_region = helper_functions.group_by(df,'region')
helper_functions.df_to_csv(spent_by_region,config.REGION_CSV)

# Calculate spent by date - Daily spent
spent_by_date = helper_functions.group_by(df,'date')
helper_functions.df_to_csv(spent_by_date,config.DAILY_SPENT_CSV)

# Save summary to output JSON
Summary = {
    'Summary':'Summary of Spent',
    'Total spending': int(total_spent),
    'Average spending': int(avg_spent),
    'Most spending': int(max_spent),
    'Least spending': int(min_spent)
}

helper_functions.json_dump(config.JSON_SUMMARY_OUTPUT,Summary)

# Monthly category ranking
monthly_category = helper_functions.mon_cat_rank(df)

# Transactions above threshold
threshold = config.DEFAULT_THRESHOLD
filtered = helper_functions.high_val_txn(threshold,df)
helper_functions.df_to_csv(filtered,config.HIGH_VAL_TXN)

# Payment Method Analysis - Pivot
pma = helper_functions.pivot_analysis(df,'payment_method')
helper_functions.df_to_csv(pma,config.PMA_CSV)

# Failed transactions report
failed = helper_functions.filter_one_level(df,'status','FAILED')
helper_functions.df_to_csv(failed,config.FAILED_CSV)

# Pending transactions report
pending = helper_functions.filter_one_level(df,'status','PENDING')
helper_functions.df_to_csv(pending,config.PENDING_CSV)
print("Exporting reports to output folder..")

pending_total = helper_functions.summarizer(pending,'amount',sum)
print("Pending Total:",pending_total)
pending_count = helper_functions.summarizer(pending,'amount',pd.Series.count)
print("Pending Count:",pending_count)

print("Analysis complete! Check the output folder for detailed results.")
end_time = time.time()
print("Pipeline executed in", end_time-start_time, "seconds")