import os
import pandas as pd

# File paths
input_excel_file = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_CAMS_PM25.xlsx"
compare_excel_file = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_datasets.csv"
output_excel_file = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_CAMS_PM25_Averaged.xlsx"

print("Reading the Excel File...")
df = pd.read_excel(input_excel_file)

print("Reading the Comparison CSV File...")
compare_df = pd.read_csv(compare_excel_file)

# Remove leading/trailing spaces from column names to prevent matching bugs
df.columns = df.columns.str.strip() 
compare_df.columns = compare_df.columns.str.strip()

# Dynamically locate the date column safely for the input file
date_col = 'valid_date' if 'valid_date' in df.columns else df.columns[0] 
df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors='coerce') 

# Dynamically locate the date column for the comparison file
compare_date_col = 'valid_date' if 'valid_date' in compare_df.columns else compare_df.columns[0]
compare_df[compare_date_col] = pd.to_datetime(compare_df[compare_date_col], dayfirst=True, errors='coerce')

df['Date_Only'] = df[date_col].dt.date
compare_df['Date_Only'] = compare_df[compare_date_col].dt.date

print("Calculating the daily average per coordinate point")
group_cols = ['Date_Only']
for col in ['latitude', 'longitude', 'lat', 'lon', 'station']:
    if col in df.columns:
        group_cols.append(col)

# Group by date AND coordinates, then average the PM2.5 values
daily_averaged_df = df.groupby(group_cols, as_index=False)['PM2.5 (ug/m3)'].mean()

print("Matching and filtering data rows based on the target dataset")
merge_keys = ['Date_Only']
for col in ['latitude', 'longitude', 'lat', 'lon']:
    if col in daily_averaged_df.columns and col in compare_df.columns:
        merge_keys.append(col)

# This filters daily_averaged_df to only rows that exist in compare_df
final_matched_df = pd.merge(daily_averaged_df, compare_df[merge_keys], on=merge_keys, how='inner')

# Clean up: Rename 'Date_Only' back to your original date column name and drop temporary column
final_matched_df[date_col] = final_matched_df['Date_Only']
final_matched_df = final_matched_df.drop(columns=['Date_Only'])

# Reorder columns to put date first
cols = [date_col] + [c for c in final_matched_df.columns if c != date_col]
final_matched_df = final_matched_df[cols]

print("Saving and Compiling...")
final_matched_df.to_excel(output_excel_file, index=False)

print(f"\nSaved the daily averaged data to:\n{output_excel_file}")
print(f"Target dataset (Bachok_datasets.csv) rows: {len(compare_df)}")
print(f"Final matched CAMS dataset rows: {len(final_matched_df)}")