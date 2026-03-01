"""Dallas County property data scraper - FIXED VERSION."""

import csv
import os
from typing import Dict, List
from app.scrapers.base_scraper import BaseScraper
from app.models import Property

class DallasScraper(BaseScraper):
    def __init__(self, db, data_dir: str = None):
        super().__init__(db, download_dir="data/dallas")
        self.data_dir = data_dir or os.path.join(self.download_dir, "extracted")
    
    def scrape(self) -> int:
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError(
                f"Data directory not found: {self.data_dir}\n"
                f"Please extract Dallas County CSV files to this location."
            )
        
        account_info = self.load_account_info()
        appraisal_values = self.load_appraisal_values()
        res_details = self.load_res_details()
        
        properties = self.join_and_create_properties(
            account_info, 
            appraisal_values, 
            res_details
        )
        
        print(f"Inserting {len(properties)} Dallas properties...")
        self.bulk_insert(properties)
        
        return len(properties)
    
    def load_account_info(self) -> Dict[str, Dict]:
        filepath = os.path.join(self.data_dir, "Account_Info.csv")
        print(f"Loading {filepath}...")
        
        accounts = {}
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                account_num = row['ACCOUNT_NUM']
                accounts[account_num] = {
                    'address': self.build_address(row),
                    'owner_name': row.get('OWNER_NAME1', '').strip(),
                    'city': row.get('PROPERTY_CITY', '').strip(),
                    'zip_code': row.get('PROPERTY_ZIPCODE', '').strip()
                }
        
        print(f"Loaded {len(accounts)} accounts")
        return accounts
    
    def build_address(self, row: Dict) -> str:
        parts = [
            row.get('STREET_NUM', '').strip(),
            row.get('FULL_STREET_NAME', '').strip(),
            row.get('UNIT_ID', '').strip()
        ]
        return ' '.join(p for p in parts if p)
    
    def load_appraisal_values(self) -> Dict[str, Dict]:
        filepath = os.path.join(self.data_dir, "Account_Appraisal_Year.csv")
        print(f"Loading {filepath}...")
        
        values = {}
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                account_num = row['ACCOUNT_NUM']
                values[account_num] = {
                    'assessed_value': self.parse_decimal(row.get('TOT_VAL', '')),
                    'land_value': self.parse_decimal(row.get('LAND_VAL', '')),
                    'impr_value': self.parse_decimal(row.get('IMPR_VAL', ''))
                }
        
        print(f"Loaded {len(values)} appraisal values")
        return values
    
    def load_res_details(self) -> Dict[str, Dict]:
        filepath = os.path.join(self.data_dir, "Res_Detail.csv")
        print(f"Loading {filepath}...")
        
        details = {}
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                account_num = row['ACCOUNT_NUM']
                details[account_num] = {
                    'square_feet': self.parse_int(row.get('TOT_LIVING_AREA_SF', '')),
                    'year_built': self.parse_int(row.get('YR_BUILT', '')),
                    'bedrooms': self.parse_int(row.get('NUM_BEDROOMS', '')),
                    'bathrooms': self.parse_decimal(row.get('NUM_FULL_BATHS', ''))
                }
        
        print(f"Loaded {len(details)} residential details")
        return details
    
    def join_and_create_properties(
        self, 
        account_info: Dict, 
        appraisal_values: Dict, 
        res_details: Dict
    ) -> List[Property]:
        properties = []
        
        for account_num, info in account_info.items():
            if not info['address']:
                continue
            
            values = appraisal_values.get(account_num, {})
            details = res_details.get(account_num, {})
            
            prop = Property(
                address=info['address'],
                owner_name=info['owner_name'],
                city=info['city'],
                zip_code=info['zip_code'],
                county="Dallas",
                assessed_value=values.get('assessed_value'),
                market_value=values.get('assessed_value'),
                square_feet=details.get('square_feet'),
                bedrooms=details.get('bedrooms'),
                bathrooms=details.get('bathrooms'),
                year_built=details.get('year_built'),
                property_type="Residential"
            )
            
            properties.append(prop)
        
        return properties
