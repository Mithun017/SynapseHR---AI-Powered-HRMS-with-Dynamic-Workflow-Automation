from sqlalchemy import text
from app.db.session import engine

def nuke():
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
        conn.commit()
    print("Database nuked successfully.")

if __name__ == "__main__":
    nuke()
