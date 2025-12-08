from pydantic import BaseModel
class ItemResult(BaseModel):
    productName: str
    price: int
    quntity: int
    owner: str