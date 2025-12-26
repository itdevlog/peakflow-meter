import sys
import os
sys.path.append('/root/peakflow-meter/backend')

# Add the app directory to the path
sys.path.append('/root/peakflow-meter/backend/app')

from app.config import settings
from app.database import engine, Base
import sqlalchemy

print(f"Database URL: {settings.database_url}")

try:
    # Test connection
    with engine.connect() as conn:
        print("Database connection successful")
        result = conn.execute(sqlalchemy.text("SELECT 1"))
        print("Basic query successful")
except Exception as e:
    print(f"Database connection failed: {e}")

try:
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")
    
    # Check what tables exist
    inspector = sqlalchemy.inspect(engine)
    tables = inspector.get_table_names()
    print(f"Existing tables: {tables}")
    
except Exception as e:
    print(f"Table creation failed: {e}")
    import traceback
    traceback.print_exc()