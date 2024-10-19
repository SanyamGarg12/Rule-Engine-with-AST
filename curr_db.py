import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Rule  # Assuming the Rule model is defined in models.py

# Replace with your PostgreSQL credentials and database
DATABASE_URI = "postgresql://rule_user:1234567@localhost:5433/rule_engine"

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Query all entries from the "rules" table
rules = session.query(Rule).all()

# Prepare the list to store the rules as dictionaries
rules_list = []

# Collect each rule entry
for rule in rules:
    rule_dict = {
        "id": str(rule.id),
        "name": rule.name,
        "ast": rule.ast,
        "created_at": str(rule.created_at)
    }
    rules_list.append(rule_dict)

# Write the rules to a JSON file
with open('RulesDB.json', 'w') as json_file:
    json.dump(rules_list, json_file, indent=4)

# Close the session
session.close()
