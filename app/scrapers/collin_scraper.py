"""Collin County property data scraper."""

import csv
import os
from typing import List
from app.scrapers.base_scraper import BaseScraper
from app.models import Property

class CollinScraper(BaseScraper):
    def __init__(self, db, csv_path: str = None):
        super().__init__(db, download_dir="data/collin")
        self.csv_path = csv_path or os.path.join(self.download_dir, "collin_data.csv")
    
    def scrape(self) -> int:
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(
                f"CSV file not found: {self.csv_path}\n"
                f"Please download Collin County CSV and place it at this location."
            )
        
        properties = self.parse_csv(self.csv_path)
        
        print(f"Inserting {len(properties)} Collin properties...")
        self.bulk_insert(properties)
        
        return len(properties)
    
    def parse_csv(self, filepath: str) -> List[Property]:
        properties = []
        
        print(f"Parsing {filepath}...")
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f, delimiter='\t')
            
            for row in reader:
                address = row.get('situsConcat', '').strip()
                if not address:
                    continue
                
                prop = Property(
                    address=address,
                    owner_name=row.get('ownerName', '').strip(),
                    city=row.get('situsCity', '').strip(),
                    zip_code=row.get('situsZip', '').strip(),
                    county="Collin",
                    assessed_value=self.parse_decimal(row.get('currValMarket', '')),
                    market_value=self.parse_decimal(row.get('currValMarket', '')),
                    square_feet=self.parse_int(row.get('imprvMainArea', '')),
                    bedrooms=None,
                    bathrooms=None,
                    year_built=self.parse_int(row.get('imprvYearBuilt', '')),
                    property_type="Residential"
                )
                
                properties.append(prop)
        
        print(f"Parsed {len(properties)} properties")
        return properties
