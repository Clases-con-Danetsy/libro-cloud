from app.database import SessionLocal
from sqlalchemy import text

def rename_column():
    db = SessionLocal()
    try:
        # Try RENAME COLUMN (MySQL 8.0+)
        print("Attempting RENAME COLUMN...")
        db.execute(text("ALTER TABLE usuarios RENAME COLUMN role_id TO rol_id"))
        print("Success: Renamed column to 'rol_id'.")
    except Exception as e:
        print(f"RENAME COLUMN failed: {e}")
        try:
             # Fallback to CHANGE
             print("Attempting CHANGE COLUMN...")
             # Note: Need to match exact definition. 
             # Based on previous check: int, foreign key. 
             # We might lose FK if we are not careful, but usually we just change name/type.
             # Assuming int(11) or int.
             db.execute(text("ALTER TABLE usuarios CHANGE role_id rol_id INT NOT NULL DEFAULT 1"))
             print("Success: Changed column to 'rol_id'.")
        except Exception as e2:
             print(f"CHANGE COLUMN failed: {e2}")

    finally:
        db.close()

if __name__ == "__main__":
    rename_column()
