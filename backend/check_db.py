from app.database import SessionLocal, engine
from sqlalchemy import text

def check_db():
    db = SessionLocal()
    try:
        # Check tables
        result = db.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        print(f"Tables found: {tables}")
        
        if 'user' in tables:
             print("ALERT: 'user' table exists!")
             # db.execute(text("DROP TABLE user")) # Uncomment to fix if needed
        else:
             print("Good: 'user' table does not exist.")

        if 'usuarios' in tables:
             print("Good: 'usuarios' table exists.")
             # Check content
             users = db.execute(text("SELECT id, username, password FROM usuarios")).fetchall()
             print("Users in 'usuarios':")
             for u in users:
                 print(u)
        else:
             print("ALERT: 'usuarios' table missing!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
