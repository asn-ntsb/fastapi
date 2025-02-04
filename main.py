from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

items_db = []

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Testing App!"}

@app.get("/items/", response_model=List[Item])
def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate):
    new_item = Item(
        id=len(items_db) + 1,  # Auto-generate ID
        name=item.name,
        description=item.description,
        price=item.price,
    )
    items_db.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate):
    existing_item = next((item for item in items_db if item.id == item_id), None)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    existing_item.name = item.name
    existing_item.description = item.description
    existing_item.price = item.price
    return existing_item

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db.remove(item)
    return item