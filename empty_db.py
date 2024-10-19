from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Rule  # Assuming the Rule model is defined in models.py
from main import DATABASE_URL as DATABASE_URI


# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

try:
    # Delete all entries from the "rules" table
    session.query(Rule).delete()
    
    # Commit the transaction
    session.commit()
    print("All entries deleted successfully.")
    
except Exception as e:
    # Rollback in case of an error
    session.rollback()
    print(f"Error occurred: {e}")
    
finally:
    # Close the session
    session.close()
