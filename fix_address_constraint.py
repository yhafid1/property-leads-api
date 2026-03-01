"""Remove unique constraint from properties address column."""

from sqlalchemy import text
from app.database.session import SessionLocal, engine

def fix_address_constraint():
    db = SessionLocal()
    
    try:
        print("Dropping unique constraint on address column...")
        
        # Drop the unique index
        with engine.connect() as conn:
            conn.execute(text("DROP INDEX IF EXISTS ix_properties_address;"))
            conn.commit()
        
        print("Constraint removed successfully!")
        print("You can now run the scraper again.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_address_constraint()
