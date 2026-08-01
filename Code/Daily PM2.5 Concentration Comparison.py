import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths direction
input_excel_file = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_CAMS_PM25_Averaged.xlsx"
compare_excel_file = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_datasets.csv"

print("Reading and parsing datasets")
df_cams = pd.read_excel(input_excel_file)
df_ref = pd.read_csv(compare_excel_file)

# Clean column names
df_cams.columns = df_cams.columns.str.strip()
df_ref.columns = df_ref.columns.str.strip()

# Identify date columns and parse with dayfirst=True to handle dd/mm/yyyy
cams_date_col = 'valid_date' if 'valid_date' in df_cams.columns else df_cams.columns[0]
ref_date_col = 'valid_date' if 'valid_date' in df_ref.columns else df_ref.columns[0]

df_cams[cams_date_col] = pd.to_datetime(df_cams[cams_date_col], dayfirst=True, errors='coerce')
df_ref[ref_date_col] = pd.to_datetime(df_ref[ref_date_col], dayfirst=True, errors='coerce')

# Drop any rows with invalid dates
df_cams = df_cams.dropna(subset=[cams_date_col])
df_ref = df_ref.dropna(subset=[ref_date_col])

# Look for PM2.5 columns dynamically
print("\nColumn Verification")
print(f"CAMS Available Columns: {list(df_cams.columns)}")
print(f"Reference Available Columns: {list(df_ref.columns)}")

# Find the PM2.5 column dynamically by looking for a partial string match (case-insensitive)
cams_pm_col = next((col for col in df_cams.columns if 'pm2' in col.lower()), None)
ref_pm_col = next((col for col in df_ref.columns if 'pm2' in col.lower()), None)

if not cams_pm_col:
    raise KeyError("Could not automatically find a PM2.5 column in the CAMS dataset.")
if not ref_pm_col:
    raise KeyError(f"Could not automatically find a PM2.5 column in Bachok_datasets.csv. Please verify its name in the printed list above.")

print(f"Using '{cams_pm_col}' for CAMS and '{ref_pm_col}' for Reference dataset.\n")

print("Processing daily averages...")
daily_cams = df_cams.groupby(df_cams[cams_date_col].dt.date)[cams_pm_col].mean().reset_index()
daily_cams.columns = ['Date', 'CAMS_PM25']

# Aggregate Reference data to daily averages (just in case it has multiple sub-day records)
daily_ref = df_ref.groupby(df_ref[ref_date_col].dt.date)[ref_pm_col].mean().reset_index()
daily_ref.columns = ['Date', 'Reference_PM25']

# Merge the two aggregated datasets on the Date index so we only plot matching timelines
merged_df = pd.merge(daily_cams, daily_ref, on='Date', how='inner')
merged_df['Date'] = pd.to_datetime(merged_df['Date']) # Convert back to datetime for plotting
merged_df = merged_df.sort_values('Date')

print("Generating line graph")
plt.figure(figsize=(14, 6))
sns.set_theme(style="whitegrid")

# Plot both lines
plt.plot(merged_df['Date'], merged_df['CAMS_PM25'], label='Bachok CAMS (Averaged)', color='#1f77b4', linewidth=2)
plt.plot(merged_df['Date'], merged_df['Reference_PM25'], label='Bachok Reference Dataset', color='#ff7f0e', linewidth=1.5, linestyle='--')

# Graph customizations
plt.title('Daily PM2.5 Concentration Comparison: CAMS vs Reference Dataset', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Date', fontsize=12)
plt.ylabel('PM2.5 Concentration ($\mu g/m^3$)', fontsize=12)
plt.legend(fontsize=11, loc='upper right')

plt.gcf().autofmt_xdate() 
plt.tight_layout()
plt.show()