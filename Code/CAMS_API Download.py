import cdsapi

#This code is to extract CAMS PM2.5 from CDS 
dataset = "cams-global-reanalysis-eac4"
request = {
    "variable": ["particulate_matter_2.5um"],
    "date": ["2014-01-12/2025-12-31"],
    "time": [
        "00:00", "03:00", "06:00",
        "09:00", "12:00", "15:00",
        "18:00", "21:00"
    ],
    "data_format": "netcdf_zip",
    # Fixed spatial grid array order: [North, West, South, East]
    "area": [6.50, 101.7, 5.50, 103]
}

client = cdsapi.Client(
    url="https://ads.atmosphere.copernicus.eu/api",
    key="71c44904-b9cb-48c3-8488-e10abd2089cd"
)

print("Connecting to Atmosphere Data Store and requesting Bachok PM2.5 data")
client.retrieve(dataset, request).download("CAMS_BACHOK_peninsular.zip")
print("Download Complete!")