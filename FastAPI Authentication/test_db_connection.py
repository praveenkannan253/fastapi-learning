from sqlalchemy import text
from app.core.database import engine

try:
    with engine.connect() as connection:
        result=connection.execute(text("SELECT 1"))

        print("Database connection successful!")
        print("Query result:", result.scalar())

except Exception as error:
     print("Database connection failed!")
     print(error)

finally:
    engine.dispose()
