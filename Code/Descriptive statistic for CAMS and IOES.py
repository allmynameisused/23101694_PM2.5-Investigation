import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# Datasets location 
file_path_CAMS = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_CAMS_PM25_Averaged.xlsx"
file_path_IOES = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Bachok_datasets.csv"
output_path = r"C:\Users\User\OneDrive\Documents\FYP code submission version\23101694_PM2.5-Investigation\Picture"
# Load datasets 
print("Reading CAMS dataset")
df = pd.read_excel(file_path_CAMS)
print("Reading IOES dataset")
dx = pd.read_csv(file_path_IOES)

# Clean column names immediately to remove trailing spaces or weird characters
df.columns = df.columns.str.strip()
dx.columns = dx.columns.str.strip()

# Handle column matching dynamically (looking for partial string matches for safety)
date_col_CAMS = 'valid_date' if 'valid_date' in df.columns else df.columns[0]
pm25_col_CAMS = [c for c in df.columns if 'PM2.5' in c or 'PM25' in c][0] if any('PM2' in c for c in df.columns) else df.columns[1]

date_col_IOES = 'date' if 'date' in dx.columns else dx.columns[0]
pm25_col_IOES = [c for c in dx.columns if 'pm25' in c or 'PM2.5' in c][0] if any('pm' in c or 'PM' in c for c in dx.columns) else dx.columns[1]

# Secure the data type is consistent 
df[date_col_CAMS] = pd.to_datetime(df[date_col_CAMS], dayfirst=True, errors='coerce')
df[pm25_col_CAMS] = pd.to_numeric(df[pm25_col_CAMS], errors='coerce')

dx[date_col_IOES] = pd.to_datetime(dx[date_col_IOES], dayfirst=True, errors='coerce')
dx[pm25_col_IOES] = pd.to_numeric(dx[pm25_col_IOES], errors='coerce')

# Drop any conversion artifacts / missing rows
df = df.dropna(subset=[date_col_CAMS, pm25_col_CAMS])
dx = dx.dropna(subset=[date_col_IOES, pm25_col_IOES])


print("\nAdvanced Statistics for CAMS Dataset:")
mean_val_CAMS = df[pm25_col_CAMS].mean()
median_val_CAMS = df[pm25_col_CAMS].median()
std_val_CAMS = df[pm25_col_CAMS].std()
var_val_CAMS = df[pm25_col_CAMS].var()
min_val_CAMS = df[pm25_col_CAMS].min()
max_val_CAMS = df[pm25_col_CAMS].max()
skew_val_CAMS = df[pm25_col_CAMS].skew()
kurt_val_CAMS = df[pm25_col_CAMS].kurt()

print(f"Mean: {mean_val_CAMS:.2f}")
print(f"Median: {median_val_CAMS:.2f}")
print(f"Standard Deviation: {std_val_CAMS:.2f}")
print(f"Variance: {var_val_CAMS:.2f}")
print(f"Minimum: {min_val_CAMS:.2f}")
print(f"Maximum: {max_val_CAMS:.2f}")
print(f"Skewness: {skew_val_CAMS:.2f}")
print(f"Kurtosis: {kurt_val_CAMS:.2f}")

print("\nAdvanced Statistics for IOES Dataset:")
mean_val_IOES = dx[pm25_col_IOES].mean()
median_val_IOES = dx[pm25_col_IOES].median()
std_val_IOES = dx[pm25_col_IOES].std()
var_val_IOES = dx[pm25_col_IOES].var()
min_val_IOES = dx[pm25_col_IOES].min()
max_val_IOES = dx[pm25_col_IOES].max()
skew_val_IOES = dx[pm25_col_IOES].skew()
kurt_val_IOES = dx[pm25_col_IOES].kurt()

print(f"Mean: {mean_val_IOES:.2f}")
print(f"Median: {median_val_IOES:.2f}")
print(f"Standard Deviation: {std_val_IOES:.2f}")
print(f"Variance: {var_val_IOES:.2f}")
print(f"Minimum: {min_val_IOES:.2f}")
print(f"Maximum: {max_val_IOES:.2f}")
print(f"Skewness: {skew_val_IOES:.2f}")
print(f"Kurtosis: {kurt_val_IOES:.2f}")

# Extract time characteristics uniformly
df['Month'] = df[date_col_CAMS].dt.month
df['DayOfWeek'] = df[date_col_CAMS].dt.day_name()

dx['Month'] = dx[date_col_IOES].dt.month
dx['DayOfWeek'] = dx[date_col_IOES].dt.day_name()


print("\n" + "="*55)
print("COMPARATIVE SEASONAL TRENDS (MONTHLY)") 
print("="*55)
cams_monthly = df.groupby('Month')[pm25_col_CAMS].mean()
ioes_monthly = dx.groupby('Month')[pm25_col_IOES].mean()

comparison_month_df = pd.DataFrame({'CAMS_Mean': cams_monthly, 'IOES_Mean': ioes_monthly})
print(comparison_month_df.to_string())

print("\n" + "="*55)
print("COMPARATIVE WEEKLY TRENDS (DAY OF WEEK)")
print("="*55)
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
cams_weekly = df.groupby('DayOfWeek')[pm25_col_CAMS].mean().reindex(days_order)
ioes_weekly = dx.groupby('DayOfWeek')[pm25_col_IOES].mean().reindex(days_order)

comparison_week_df = pd.DataFrame({'CAMS_Mean': cams_weekly, 'IOES_Mean': ioes_weekly})
print(comparison_week_df.to_string())


print("\nGenerating comparative visualization assets")

# Plot 1: Combined Time-Series Comparison
plt.figure(figsize=(14, 6))
plt.plot(df[date_col_CAMS], df[pm25_col_CAMS], label='CAMS (Reanalysis Model)', color='teal', alpha=0.8, linewidth=1.5)
plt.plot(dx[date_col_IOES], dx[pm25_col_IOES], label='IOES (Ground Station)', color='darkorange', alpha=0.7, linewidth=1.5)
plt.title('Daily PM2.5 Concentration: CAMS vs IOES Timeline Comparison', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('PM2.5 (ug/m³)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'cams_vs_ioes_timeline.png'), dpi=300)
plt.close()

# Plot 2: Monthly Pattern Comparison (Melting safely)
df_melt = pd.DataFrame(list(zip(df['Month'], df[pm25_col_CAMS], ['CAMS']*len(df))) +
                       list(zip(dx['Month'], dx[pm25_col_IOES], ['IOES']*len(dx))),
                       columns=['Month', 'PM2.5', 'Source'])

plt.figure(figsize=(10, 5))
sns.barplot(data=df_melt, x='Month', y='PM2.5', hue='Source', palette=['teal', 'darkorange'], errorbar='ci')
plt.title('Monthly Seasonal Variations: CAMS vs IOES', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Average PM2.5 (ug/m³)')
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'cams_vs_ioes_monthly_pattern.png'), dpi=300)
plt.close()

# Distribution Density Overlay
plt.figure(figsize=(10, 5))
sns.kdeplot(df[pm25_col_CAMS], fill=True, color="teal", label="CAMS Data Density", alpha=0.4, clip=(0, None))
sns.kdeplot(dx[pm25_col_IOES], fill=True, color="darkorange", label="IOES Data Density", alpha=0.4, clip=(0, None))
plt.title('Data Distribution Profile: CAMS vs IOES', fontsize=14, fontweight='bold')
plt.xlabel('PM2.5 Concentration (ug/m³)')
plt.ylabel('Density')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'cams_vs_ioes_distribution.png'), dpi=300)
plt.close()

print(f"\nAnalysis complete! Visual validation charts saved directly to:")
print(f"1. Timeline Track  : {os.path.join(output_path, 'cams_vs_ioes_timeline.png')}")
print(f"2. Seasonal Peaks : {os.path.join(output_path, 'cams_vs_ioes_monthly_pattern.png')}")
print(f"3. Density Profiles: {os.path.join(output_path, 'cams_vs_ioes_distribution.png')}")