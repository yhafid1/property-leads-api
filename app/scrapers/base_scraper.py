"""Base scraper class with shared functionality for all county scrapers."""

import requests
import zipfile
import csv
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models import Property
from decimal import Decimal
from datetime import datetime

class BaseScraper(ABC):
    def __init__(self, db: Session, download_dir: str = "data/downloads"):
        self.db = db
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)
    
    @abstractmethod
    def scrape(self) -> int:
        pass
    
    def download_file(self, url: str, filename: str) -> str:
        filepath = os.path.join(self.download_dir, filename)
        
        print(f"Downloading {filename}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded to {filepath}")
        return filepath
    
    def extract_zip(self, zip_path: str, extract_to: str) -> str:
        print(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted to {extract_to}")
        return extract_to
    
    def parse_decimal(self, value: str) -> Optional[Decimal]:
        if not value or value.strip() == '':
            return None
        try:
            cleaned = value.replace(',', '').strip()
            return Decimal(cleaned)
        except:
            return None
    
    def parse_int(self, value: str) -> Optional[int]:
        if not value or value.strip() == '':
            return None
        try:
            return int(value.replace(',', '').strip())
        except:
            return None
    
    def parse_date(self, value: str) -> Optional[datetime]:
        if not value or value.strip() == '':
            return None
        try:
            return datetime.strptime(value, '%m/%d/%Y').date()
        except:
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except:
                return None
    
    def bulk_insert(self, properties: List[Property], batch_size: int = 1000):
        total = len(properties)
        for i in range(0, total, batch_size):
            batch = properties[i:i+batch_size]
            self.db.bulk_save_objects(batch)
            self.db.commit()
            print(f"Inserted {min(i+batch_size, total)}/{total} properties")
