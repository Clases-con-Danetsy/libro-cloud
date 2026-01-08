from app.database import SessionLocal
from sqlalchemy import text

def check_columns():
    db = SessionLocal()
    try:
        # Try MySQL syntax
        result = db.execute(text("DESCRIBE usuarios"))
        columns = [row[0] for row in result]
        print(f"Columns in usuarios: {columns}")
    except Exception:
        try:
            # Try SQLite syntax
            result = db.execute(text("PRAGMA table_info(usuarios)"))
            columns = [row[1] for row in result]
            print(f"Columns in usuarios: {columns}")
        except Exception as e:
            print(f"Error checking columns: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_columns()
