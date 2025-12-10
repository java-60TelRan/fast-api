from fastapi import Depends, FastAPI, HTTPException, Header, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from models.item import Item
from models.item_result import ItemResult
from logger import logger
ITEMS_DB: list[ItemResult] = []
API_KEYS = {
    "token-user": {"role": "user", "username":"user"},
    "token-admin": {"role": "admin", "username":"admin"}
}
app = FastAPI()
async def getCurrentUser(x_api_key: str = Header(..., alias="X-API-KEY")):
    user = API_KEYS.get(x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication error")
    return user
async def getAdmin(user=Depends(getCurrentUser)):
    if user["role"]  != "admin":
        raise HTTPException(status_code=403, detail="Access Denied") 
    return user
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    logger.info("method: %s, path: %s, port: %s", request.method, request.url.path, request.url.port)
    resp: Response = await call_next(request)
    logger.info("status code: %s", resp.status_code)
    return resp
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
async def create_item(item: Item, user=Depends(getCurrentUser)):
    logger.debug("product name: %s, price: %s, quantity: %s",
                 item.productName, item.price, item.quantity)
    itemRes: ItemResult = ItemResult(
        productName=item.productName,
        price=item.price,
        quntity=item.quantity,
        owner=user["username"]
        
    )
    ITEMS_DB.append(itemRes)
    return itemRes
@app.get("/items")
async def getItems(user=Depends(getAdmin)):
    return ITEMS_DB
    