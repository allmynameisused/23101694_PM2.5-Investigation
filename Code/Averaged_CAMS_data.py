import os
import pandas as pd

# File paths
input_excel_file = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_subsetted_CAMS\Bachok_CAMS_PM25.xlsx"
compare_excel_file = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_datasets.csv"
output_excel_file = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_subsetted_CAMS\Bachok_CAMS_PM25_Averaged.xlsx"

print("Reading the Excel File")
df = pd.read_excel(input_excel_file)

print("Reading the Comparison CSV File")
compare_df = pd.read_csv(compare_excel_file)

df.columns = df.columns.str.strip() 
compare_df.columns = compare_df.columns.str.strip()

# Dynamically locate the date column safely for the input file
date_col = 'valid_date' if 'valid_date' in df.columns else df.columns[0] 
df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors='coerce') 

# Dynamically locate the date column for the comparison file
compare_date_col = 'valid_date' if 'valid_date' in compare_df.columns else compare_df.columns[0]
compare_df[compare_date_col] = pd.to_datetime(compare_df[compare_date_col], dayfirst=True, errors='coerce')
print("Matching and filtering data points based on dates...")
allowed_dates = compare_df[compare_date_col].dt.date.unique()

filtered_df = df[df[date_col].dt.date.isin(allowed_dates)]

print("Calculating the daily average per coordinate point")
daily_df = filtered_df.groupby(filtered_df[date_col].dt.date)['PM2.5 (ug/m3)'].mean().reset_index()

print("Saving the processed data into Excel")
daily_df.to_excel(output_excel_file, index=False)

print(f"\nSuccessfully saved the daily averaged data to:\n{output_excel_file}")
print(f"Original dataset: {len(df)} 3-hourly rows.")
print(f"Filtered & condensed dataset: {len(daily_df)} clean daily records matching the target dataset.")