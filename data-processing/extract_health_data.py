"""
Apple Health Data Extractor
Converts Apple Health export.xml to CSV files for analysis
"""

import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz

def extract_health_data(xml_path='export.xml', days=90):
    """
    Extract the last N days of health data from Apple Health export
    
    Args:
        xml_path: Path to export.xml file
        days: Number of days to extract (default 90)
    """
    print(f"📊 Extracting last {days} days of health data...")
    print("This may take 2-3 minutes for large files...\n")
    
    # Parse XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Calculate cutoff date
    tz = pytz.UTC
    cutoff = (datetime.now(tz) - timedelta(days=days)).strftime('%Y-%m-%d')
    print(f"Extracting data from {cutoff} onwards...\n")
    
    # Extract HRV data
    print("Extracting HRV data...")
    hrv_data = []
    for record in root.findall('.//Record[@type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN"]'):
        if record.get('startDate', '') >= cutoff:
            hrv_data.append({
                'date': record.get('startDate'),
                'hrv': record.get('value')
            })
    pd.DataFrame(hrv_data).to_csv('hrv.csv', index=False)
    print(f"✓ Created hrv.csv with {len(hrv_data)} records")
    
    # Extract Resting Heart Rate
    print("Extracting Resting HR data...")
    rhr_data = []
    for record in root.findall('.//Record[@type="HKQuantityTypeIdentifierRestingHeartRate"]'):
        if record.get('startDate', '') >= cutoff:
            rhr_data.append({
                'date': record.get('startDate'),
                'resting_hr': record.get('value')
            })
    pd.DataFrame(rhr_data).to_csv('resting_hr.csv', index=False)
    print(f"✓ Created resting_hr.csv with {len(rhr_data)} records")
    
    # Extract Sleep Data
    print("Extracting Sleep data...")
    sleep_data = []
    for record in root.findall('.//Record[@type="HKCategoryTypeIdentifierSleepAnalysis"]'):
        if record.get('startDate', '') >= cutoff:
            sleep_data.append({
                'start': record.get('startDate'),
                'end': record.get('endDate'),
                'value': record.get('value')
            })
    pd.DataFrame(sleep_data).to_csv('sleep.csv', index=False)
    print(f"✓ Created sleep.csv with {len(sleep_data)} records")
    
    # Extract Active Calories
    print("Extracting Calories data...")
    cal_data = []
    for record in root.findall('.//Record[@type="HKQuantityTypeIdentifierActiveEnergyBurned"]'):
        if record.get('startDate', '') >= cutoff:
            cal_data.append({
                'date': record.get('startDate'),
                'calories': record.get('value')
            })
    pd.DataFrame(cal_data).to_csv('calories.csv', index=False)
    print(f"✓ Created calories.csv with {len(cal_data)} records")
    
    print("\n🎉 All done! Your CSV files are ready.")

if __name__ == "__main__":
    # Run with default settings (90 days)
    extract_health_data()
```
