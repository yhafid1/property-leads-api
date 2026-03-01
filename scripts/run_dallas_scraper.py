"""Run Dallas County scraper manually."""

from app.database.session import SessionLocal
from app.scrapers.dallas_scraper import DallasScraper

def main():
    db = SessionLocal()
    
    try:
        scraper = DallasScraper(db)
        count = scraper.scrape()
        print(f"\nSuccess! Imported {count} Dallas County properties")
    except Exception as e:
        print(f"\nError: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
