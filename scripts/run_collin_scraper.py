"""Run Collin County scraper manually."""

from app.database.session import SessionLocal
from app.scrapers.collin_scraper import CollinScraper

def main():
    db = SessionLocal()
    
    try:
        scraper = CollinScraper(db)
        count = scraper.scrape()
        print(f"\nSuccess! Imported {count} Collin County properties")
    except Exception as e:
        print(f"\nError: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
