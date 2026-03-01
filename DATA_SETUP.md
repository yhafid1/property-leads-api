"""Manual Data Setup Guide

This guide explains how to manually download county data files and place them 
for the scrapers to process.

## Directory Structure

Create these directories in your project:

dfw-property-leads-api/
└── data/
    ├── dallas/
    │   └── extracted/          (Place Dallas CSV files here)
    │       ├── Account_Info.csv
    │       ├── Account_Appraisal_Year.csv
    │       └── Res_Detail.csv
    └── collin/
        └── collin_data.csv     (Place Collin CSV here)

## Dallas County Data

1. Go to: https://www.dallascad.org/dataproducts.aspx

2. Download: "2025 Certified Data Files with Supplemental Changes"
   (Look for DCAD2025_CURRENT.ZIP)

3. Extract the ZIP file

4. Copy these 3 files to data/dallas/extracted/:
   - Account_Info.csv
   - Account_Appraisal_Year.csv
   - Res_Detail.csv

5. Run: python scripts/run_dallas_scraper.py

## Collin County Data

1. Go to: https://data.texas.gov/stories/s/mz7k-urqw

2. Click "Export" or "Download"

3. Choose "CSV" format

4. Save as: data/collin/collin_data.csv

5. Run: python scripts/run_collin_scraper.py

## Creating Directories

Windows Command Prompt:
```cmd
cd C:\Users\yasee\Documents\dfw-property-leads-api
mkdir data\dallas\extracted
mkdir data\collin
```

## Troubleshooting

Problem: "FileNotFoundError: data/dallas/extracted/Account_Info.csv"
Solution: Make sure you extracted the CSV files to the exact path above

Problem: "No such file or directory: data/collin"
Solution: Create the directories first (see commands above)

Problem: Scraper runs but finds 0 properties
Solution: Check that CSV files have data and aren't corrupted

## File Sizes (Approximate)

Dallas:
- Account_Info.csv: ~50 MB
- Account_Appraisal_Year.csv: ~30 MB
- Res_Detail.csv: ~40 MB

Collin:
- collin_data.csv: ~80 MB

## How Often to Update

Real estate data doesn't change daily. Recommended schedule:
- Monthly: Download fresh data
- Weekly: If actively finding leads
- Quarterly: Minimum for accurate market data
"""