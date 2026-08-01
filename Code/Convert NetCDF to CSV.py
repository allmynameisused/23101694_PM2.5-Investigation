import os
import zipfile
import xarray as xr
import pandas as pd

zip_path = r"C:\Users\User\OneDrive\Documents\Fyp coding\CAMS_BACHOK_Data.zip"
extract_dir = r"C:\Users\User\OneDrive\Documents\Fyp coding\Bachok_subsetted_CAMS\CAMS_NETCDF_FILE"
excel_output_path = r"C:\Users\User\OneDrive\Documents\Fyp coding\Bachok_subsetted_CAMS\Bachok_CAMS_PM25.xlsx"
csv_output_path = r"C:\Users\User\OneDrive\Documents\Fyp coding\Bachok_subsetted_CAMS\Bachok_CAMS_PM25.csv"

# Extract the ZIP file automatically
print(" Step 1: Extracting NetCDF file from ZIP archive...")
if not os.path.exists(zip_path):
    raise FileNotFoundError(f"Could not find the zip file at {zip_path}. Please check your download path.")

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Find the extracted .nc file inside the folder
extracted_files = os.listdir(extract_dir)
nc_files = [f for f in extracted_files if f.endswith('.nc')]

if not nc_files:
    raise FileNotFoundError("No NetCDF (.nc) file found inside the extracted zip archive.")

nc_file_path = os.path.join(extract_dir, nc_files[0])
print(f"   Found extracted NetCDF file: {nc_files[0]}")

# Open the dataset with Xarray
print("\n Step 2: Loading NetCDF multi-dimensional data...")
ds = xr.open_dataset(nc_file_path)

# Automatically look for the PM2.5 variable name 
pm25_var = [var for var in ds.data_vars if 'pm' in var.lower() or '2p5' in var.lower()]
pm25_var_name = pm25_var[0] if pm25_var else list(ds.data_vars.keys())[0]
print(f"   Identified PM2.5 variable: '{pm25_var_name}'")

# 4. Convert units: CAMS defaults to kg/m³ but research needs µg/m³
print("\n Step 3: Converting units from kg/m³ to µg/m³...")
ds[pm25_var_name] = ds[pm25_var_name] * 1e9

# 5. Flatten the multi-dimensional structure to a DataFrame
print("\n Step 4: Unpacking dimensions (time, latitude, longitude) into table rows...")
df = ds.to_dataframe().reset_index()

df.columns = df.columns.str.strip()
df = df.rename(columns={pm25_var_name: 'PM2.5 (ug/m3)'})
original_rows = len(df)

print("\n Filtering dataset to remove 102.0 longitude records...")
df = df.loc[df['longitude'] != 102.0].copy()

total_rows = len(df)
print(f"   Original rows: {original_rows:,}")
print(f"   Rows remaining after removing 102.0 longitude: {total_rows:,}")
print(f"   Rows deleted: {original_rows - total_rows:,}")


print("\n Step 5: Exporting data...")
if total_rows < 1000000:
    print("   Row count is safe for Excel. Writing to .xlsx file...")
    df.to_excel(excel_output_path, sheet_name="Peninsular PM2.5", index=False)
    print(f"SUCCESS! Your processed Excel file is saved at:\n{excel_output_path}")
else:
    print("WARNING: Data exceeds 1 million rows! Excel will crash or truncate this data.")
    print("   Switching safe fallback to CSV format...")
    df.to_csv(csv_output_path, index=False)
    print(f"SUCCESS! Your data was safely exported as a CSV file to prevent data loss:\n{csv_output_path}")