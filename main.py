# main.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Any
import uuid
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from models import Base, Rule  # Ensure models.py is in the same directory
import ast_parser  # Ensure ast_parser.py is correctly implemented
from datetime import datetime
from typing import Optional
from fastapi.responses import FileResponse
import subprocess
# Initialize FastAPI application
app = FastAPI(title="3-Tier Rule Engine with AST")

# -----------------------
# Database Configuration
# -----------------------

# PostgreSQL connection string
DATABASE_URL = "postgresql://rule_user:1234567@localhost:5433/rule_engine"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

# -----------------------
# Pydantic Models
# -----------------------
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict it to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RuleCreate(BaseModel):
    name: str
    rule_string: str

class RuleResponse(BaseModel):
    id: uuid.UUID
    name: str
    ast: Any
    created_at: datetime
    updated_at: Optional[datetime]

class CombineRulesRequest(BaseModel):
    rule_ids: List[uuid.UUID]
    name: Optional[str] = None  # Optional name for the combined rule

class CombinedRuleResponse(BaseModel):
    id: uuid.UUID
    name: str
    combined_ast: Any
    created_at: datetime

class EvaluateRuleRequest(BaseModel):
    combined_ast: Any
    user_data: dict

class EvaluateRuleResponse(BaseModel):
    is_eligible: bool

# -----------------------
# Dependency
# -----------------------

def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# API Endpoints
# -----------------------

@app.post("/create_rule", response_model=RuleResponse, summary="Create a new rule")
def create_rule(rule: RuleCreate, db: Session = Depends(get_db)):
    """
    Create a new rule by parsing the rule string into an AST and storing it in the database.
    """
    try:
        # Parse the rule string into an AST
        parsed_ast = ast_parser.parse_rule(rule.rule_string.upper())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing rule: {str(e)}")
    
    # Check if a rule with the same name already exists
    existing_rule = db.query(Rule).filter(Rule.name == rule.name).first()
    if existing_rule:
        raise HTTPException(status_code=400, detail="Rule with this name already exists.")
    
    # Create a new Rule instance
    new_rule = Rule(
        name=rule.name,
        ast=parsed_ast
    )
    
    # Add and commit the new rule to the database
    try:
        db.add(new_rule)
        db.commit()
        db.refresh(new_rule)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return RuleResponse(
        id=new_rule.id,
        name=new_rule.name,
        ast=new_rule.ast,
        created_at=new_rule.created_at,
        updated_at=new_rule.updated_at
    )

@app.post("/combine_rules", response_model=CombinedRuleResponse, summary="Combine multiple rules into a single AST")
def combine_rules(request: CombineRulesRequest, db: Session = Depends(get_db)):
    """
    Combine multiple rules into a single AST using logical AND and store it in the database.
    """
    try:
        # Retrieve the rules from the database
        rules = db.query(Rule).filter(Rule.id.in_(request.rule_ids)).all()
        if not rules:
            raise HTTPException(status_code=404, detail="No rules found for the given IDs.")
        
        # Extract ASTs from the rules
        asts = [rule.ast for rule in rules]
        
        # Combine the ASTs
        combined_ast = ast_parser.combine_asts(asts)
        
        # Create a unique name if not provided
        combined_rule_name = request.name or f"combined_rule_{uuid.uuid4()}"
        
        # Create a new Rule instance for the combined rule
        combined_rule = Rule(
            name=combined_rule_name,
            ast=combined_ast
        )
        
        # Add and commit the combined rule to the database
        db.add(combined_rule)
        db.commit()
        db.refresh(combined_rule)

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error combining rules: {str(e)}")
    
    return CombinedRuleResponse(
        id=combined_rule.id,
        name=combined_rule.name,
        combined_ast=combined_rule.ast,
        created_at=combined_rule.created_at
    )


@app.post("/evaluate_rule", response_model=EvaluateRuleResponse, summary="Evaluate user data against a combined AST")
def evaluate_rule(request: EvaluateRuleRequest):
    """
    Evaluate the combined AST against the provided user data to determine eligibility.
    """
    try:
        # Evaluate the AST with the user data
        is_eligible = ast_parser.evaluate_ast(request.combined_ast, request.user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error evaluating rule: {str(e)}")
    
    return EvaluateRuleResponse(is_eligible=is_eligible)

@app.post("/database", summary="Generate the database file RulesDB.json")
async def database():
    """Run the curr_db.py script to generate the database.json file."""
    try:
        # Run the curr_db.py script
        subprocess.run(["python", "curr_db.py"], check=True)
        return FileResponse("RulesDB.json", media_type='application/json')
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error running script: {e}")

# -----------------------
# Root Endpoint
# -----------------------

@app.get("/", summary="Root Endpoint")
def read_root():
    return {"message": "Welcome to the 3-Tier Rule Engine with AST!"}