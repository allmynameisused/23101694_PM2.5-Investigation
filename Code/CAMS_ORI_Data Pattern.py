import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#This script is to generate descriptive statistic for Original CAMS PM2.5 dataset 
#Set visual style for plots
sns.set_theme(style="whitegrid")

#File path to your dataset
file_path = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_CAMS_PM25.xlsx"
output_dir = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Picture"

print("Reading the Excel File...")
df = pd.read_excel(file_path)

#Clean column names
df.columns = df.columns.str.strip()

#Safely locate the date and PM2.5 columns
date_col = 'valid_date' if 'valid_date' in df.columns else df.columns[0]
pm25_col = 'PM2.5 (ug/m3)' if 'PM2.5 (ug/m3)' in df.columns else [c for c in df.columns if 'PM2.5' in c or 'PM25' in c][0]

#Securely convert types
df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors='coerce')
df[pm25_col] = pd.to_numeric(df[pm25_col], errors='coerce')

#Drop empty rows to avoid calculation distortion
df = df.dropna(subset=[date_col, pm25_col])

#Convert UTC to local Malaysian time (UTC+8)
df['local_time'] = pd.to_datetime(df[date_col]) + pd.to_timedelta(8, unit='h')

#Create the 'Hour' column so it can be used for grouping and plotting
df['Hour'] = df['local_time'].dt.hour
df['Month'] = df['local_time'].dt.month
df['DayOfWeek'] = df['local_time'].dt.day_name()


print("\n" + "="*55)
print("             OVERALL STATISTICAL PATTERNS             ")
print("="*55)

mean_val = df[pm25_col].mean()
median_val = df[pm25_col].median()
mode_val = df[pm25_col].mode().iloc[0] if not df[pm25_col].mode().empty else "N/A"
std_val = df[pm25_col].std()
var_val = df[pm25_col].var()
min_val = df[pm25_col].min()
max_val = df[pm25_col].max()
skew_val = df[pm25_col].skew()
kurt_val = df[pm25_col].kurt()

print(f"Mean (Average Value)          : {mean_val:.2f} ug/m3")
print(f"Median (50th Percentile)      : {median_val:.2f} ug/m3")
print(f"Mode (Most Frequent Value)    : {mode_val} ug/m3")
print(f"Standard Deviation (Volatility): {std_val:.2f} ug/m3")
print(f"Variance (Spread)             : {var_val:.2f}")
print(f"Minimum Recorded Value        : {min_val:.2f} ug/m3")
print(f"Maximum Recorded Value        : {max_val:.2f} ug/m3")
print(f"Skewness (Distribution Shape) : {skew_val:.2f}")
print(f"Kurtosis (Outlier Frequency)  : {kurt_val:.2f}")
print("="*55)

#Diagnostic interpretation of shapes
print("\n--- Shape Insights ---")
if skew_val > 1:
    print("• High Positive Skewness: The baseline pollution is usually low, but severe, short-term pollution spike events occur frequently.")
elif -1 <= skew_val <= 1:
    print("• Symmetrical Distribution: Pollution values follow a balanced, normal curve distribution.")

if kurt_val > 0:
    print("• Leptokurtic (Heavy Tails): Extreme anomalies / hazardous air quality days occur more often than normally expected.")


print("\n" + "="*55)
print("             TIME-SERIES PATTERNS SUMMARY             ")
print("="*55)

print("\n[Diurnal Pattern] Average PM2.5 by Hour of Day (Local Malaysian Time):")
print(df.groupby('Hour')[pm25_col].mean().to_string())

print("\n[Seasonal Pattern] Average PM2.5 by Month:")
print(df.groupby('Month')[pm25_col].mean().to_string())

print("\n[Weekly Pattern] Average PM2.5 by Day of Week:")
print(df.groupby('DayOfWeek')[pm25_col].mean().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
).to_string())


print("\nGenerating visual pattern assets...")


fig, axes = plt.subplots(1, 2, figsize=(15, 5))
sns.histplot(df[pm25_col], kde=True, ax=axes[0], color='skyblue')
axes[0].set_title('PM2.5 Frequency Distribution')
axes[0].set_xlabel('Concentration (ug/m3)')

sns.boxplot(x=df[pm25_col], ax=axes[1], color='lightcoral')
axes[1].set_title('Outlier and Quantile Spread')
axes[1].set_xlabel('Concentration (ug/m3)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'pm25_distribution_patterns.png'), dpi=300)
plt.close()


plt.figure(figsize=(10, 5))
df_sorted_hours = df.sort_values('Hour')
sns.lineplot(x='Hour', y=pm25_col, data=df_sorted_hours, marker='o', color='teal', errorbar='ci')
plt.title('Diurnal Cycle (Hourly Changes in PM2.5 Profile - Local Time)')
plt.xlabel('Hour of the Day (Local Time)')
plt.ylabel('Average PM2.5 (ug/m3)')
plt.xticks(sorted(df['Hour'].unique()))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'pm25_hourly_trend.png'), dpi=300)
plt.close()


plt.figure(figsize=(10, 5))
df_sorted_months = df.sort_values('Month')
sns.barplot(x='Month', y=pm25_col, data=df_sorted_months, hue='Month', palette='viridis', legend=False, errorbar='ci')
plt.title('Monthly / Seasonal Fluctuations (Monsoonal Variations)')
plt.xlabel('Month')
plt.ylabel('Average PM2.5 (ug/m3)')
plt.xticks(ticks=range(len(sorted(df['Month'].unique()))), labels=sorted(df['Month'].unique()))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'pm25_monthly_trend.png'), dpi=300)
plt.close()

print(f"\nAnalysis complete! Visual charts have been saved directly to your folder:")
print(f"1. {os.path.join(output_dir, 'pm25_distribution_patterns.png')}")
print(f"2. {os.path.join(output_dir, 'pm25_hourly_trend.png')}")
print(f"3. {os.path.join(output_dir, 'pm25_monthly_trend.png')}")