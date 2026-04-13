import json
from schema.db import Database

db: Database | None = None

def init_db():
    with open("./app/db/db.json", "r") as f:
        global db
        db = json.loads(f.read())

def get_db():
    if not db:
        raise ValueError("DB is not initialized")
    
    return db