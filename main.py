from enum import Enum
from http.client import HTTPException
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

app = FastAPI()


class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category


# This is our database.  Will represent a real database that we would pull data from to send to the requester
items = {
    0: Item(name = "Powermatic15inchHelical Head Planer", price = 3499.99, count = 5, id = 0, category = Category.TOOLS),
    1: Item(name = "Powermatic19688inchHelicalHeadJointer", price = 75.00, count = 1, id = 1, category = Category.TOOLS),
    2: Item(name = "Titebond10ozWoodGlue", price = 8.99, count = 25, id = 2, category = Category.CONSUMABLES)
}


# FastAPI handles JSON serialization and de- for us.
# We can just use built-in python and Pydantic types. In this case dict[int, Item]
@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items} 


@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if (item_id not in items):
        raise HTTPException(status_code = 404, detail = f"Item with {item_id=} does not exist.")
    return items[item_id]


# Function parameters that are not path parameters can be specified as query parameters in ...
# Here we can query items like this /items?count=20
Selection = dict[ # dict containing the user's query argument
    str, str | int | float | Category | None
]


# QUERY PARAMETERS
# Need to add the / for query parameters.  See the route (items/)
# declaring and implementing a function in a function.....   cool.
# Look at the accepted parameters (passed by the query parameters).  If anything is declared, it gets it, 
#   if not, it will set to none.
# The check_item function (which is in a function (for scope control?)) is checking the given item by properties.
#   If any of the given properties are equal to what is given by the query parameters, it will return true.
# selection is getting each item in the items dictionary (our db), if it passes the check_item function.
# 

@app.get("/items/")
def query_item_by_parameters(
    name: str | None = None, 
    price: float | None = None, 
    count: int | None = None, 
    category: Category | None = None, 
) -> dict[str, Selection | list[Item]]:
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count != count, # why is this not equal??? check the tut, but it totally shouold be == right?
                category is None or item.category is category,
            )
        )
    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }


# idk what this does yet..
@app.post("/")
def add_item(item: Item) -> dict[str, Item]:
    if item.id in items:
        HTTPException(status_code=400, detail=f"Item with {item.id=} already exists.")

    items[item.id] = item
    return {"added": item}