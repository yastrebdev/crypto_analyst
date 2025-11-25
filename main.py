from sqlalchemy import text
from db.connect import SessionLocal

def test_db_connection():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1"))
        print("Подключение успешно, результат:", result.fetchone())
    except Exception as e:
        print("Ошибка подключения:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_db_connection()
