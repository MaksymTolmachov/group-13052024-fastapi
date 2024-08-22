from fastapi import FastAPI, status
from pydantic import BaseModel, HttpUrl, Field

from schemas import NewProduct


app = FastAPI(
    debug=True,
    title="Group13/05/2024"
)


@app.get("/")
def index():
    return {"subject": "Hello!"}


# CRUD




@app.post("/api/product/", description="create product", status_code=status.HTTP_201_CREATED, tags=["API", "Products"])
def add_product(data: NewProduct) -> dict:
    print(data)
    return {}
