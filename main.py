from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Portfolio Task Tracker API", version="1.0.0")

# In-memory database simulation (swap with SQLModel/SQLite as you grow)
db = []

# Data Validation Models (Pydantic)
class ItemCreate(BaseModel):
    title: str = Field(..., min_length=3, example="Build FastAPI Portfolio")
    description: Optional[str] = Field(None, example="Create REST endpoints and push to GitHub")
    completed: bool = False

class ItemResponse(ItemCreate):
    id: int

@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": "API is online", "status": status.HTTP_200_OK}

@app.post("/api/v1/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(item: ItemCreate):
    new_item = item.dict()
    new_item["id"] = len(db) + 1
    db.append(new_item)
    return new_item

@app.get("/api/v1/items", response_model=List[ItemResponse], tags=["Items"])
def get_items():
    return db

@app.get("/api/v1/items/{item_id}", response_model=ItemResponse, tags=["Items"])
def get_item(item_id: int):
    for item in db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")