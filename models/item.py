from pydantic import BaseModel, Field
class Item(BaseModel):
    productName: str = Field(..., min_length=3, max_length=10)
    price: int = Field(..., gt=1)
    quantity: int = Field(..., gt=0, lt=1000)