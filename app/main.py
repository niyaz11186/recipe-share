# from fastapi import FastAPI
# from pydantic import BaseModel
# from database import SessionLocal, engine
# from models import Recipe



# app = FastAPI()



# # Pydantic models for request and response
# class RecipeIn(BaseModel):
#     title: str
#     description: str
#     ingredients: str
#     instructions: str

# class RecipeOut(RecipeIn):
#     id: int

# # Create CRUD operations
# @app.post("/recipes/", response_model=RecipeOut)
# def create_recipe(recipe: RecipeIn):
#     db = SessionLocal()
#     db_recipe = Recipe(**recipe.dict())
#     db.add(db_recipe)
#     db.commit()
#     db.refresh(db_recipe)
#     db.close()
#     return db_recipe

# @app.get("/recipes/{recipe_id}", response_model=RecipeOut)
# def read_recipe(recipe_id: int):
#     db = SessionLocal()
#     recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
#     db.close()
#     return recipe

# # Add more CRUD operations as needed (update, delete, list)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI
from pydantic import BaseModel
from .database import SessionLocal
from .models import Recipe
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

app = FastAPI()

class RecipeIn(BaseModel):
    title: str
    description: str
    ingredients: str
    instructions: str

class RecipeOut(RecipeIn):
    id: int

@app.post("/recipes/", response_model=RecipeOut)
def create_recipe(recipe: RecipeIn):
    db = SessionLocal()
    db_recipe = Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    db.close()
    return db_recipe

@app.get("/recipes/{recipe_id}", response_model=RecipeOut)
def read_recipe(recipe_id: int):
    db = SessionLocal()
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    db.close()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
