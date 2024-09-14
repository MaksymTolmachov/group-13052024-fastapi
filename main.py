from fastapi import FastAPI, status, Query, Path

from schemas import NewTravel, SavedTravel, TravelPrice, DeletedTravel
from storage import storage

app = FastAPI(
    debug=True,
    title='My travel agency project',
)


@app.post('/', include_in_schema=False)
def index():
    return {'subject': "I tried my best"}


@app.post('/api/travel/', description='create new travel', status_code=status.HTTP_201_CREATED, tags=['API', 'Travel'])
def add_Travel(new_travel: NewTravel) -> SavedTravel:
    saved_travel = storage.create_travel(new_travel)
    return saved_travel


# READ
@app.get('/api/Travel/', tags=['API', 'Travel'])
def get_travel(
        limit: int = Query(default=10, description='No more than 10 Travels', gt=0), q: str = '',
) -> list[SavedTravel]:
    result = storage.get_travel(limit=limit, q=q)
    return result


@app.get('/api/travel/{travel_id}', tags=['API', 'travel'])
def get_travel(product_id: int = Path(ge=1, description='product id')) -> SavedTravel:
    result = storage.get_travel(travel_id)
    return result


# UPDATE
@app.patch('/api/travel/{travel_id}', tags=['API', 'Travel'])
def update_product_price(new_price: TravelPrice,
                         product_id: int = Path(ge=1, description='travel id')) -> SavedTravel:
    result = storage.update_travel_price(travel_id, new_price=new_price.price)
    return result


# DELETE
@app.delete('/api/travel/{travel_id}', tags=['API', 'Travel'])
def update_travel_price(travel_id: int = Path(ge=1, description='travel id')) -> DeletedTravel:
    storage.delete_travel(travel_id)
    return DeletedTravel(id=travel_id)
