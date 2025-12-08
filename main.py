from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from models.item import Item
from models.item_result import ItemResult
ITEMS_DB: list[ItemResult] = []
app = FastAPI()
@app.exception_handler(RequestValidationError)
async def requestValidationHandler(req: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail":exc.errors(),
            
            
        }
    )
@app.exception_handler(ValidationError) 
async def errorFromServer(req: Request, exc: ValidationError) :
    return JSONResponse(
        status_code=500,
        content={
            "detail": exc.errors()
        }
        
    )  
@app.get("/health")
async def health():
    return {"status": "running"}
@app.post("/items")
async def create_item(item: Item):
    itemRes: ItemResult = ItemResult(
        productName=item.productName,
        price=item.price,
        quntity=item.quantity,
        owner="user"
        
    )
    ITEMS_DB.append(itemRes)
    return itemRes
@app.get("/items")
async def getItems():
    return ITEMS_DB
    