from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator
class Item(BaseModel):
    productName: str = Field(..., min_length=3, max_length=10)
    price: int = Field(..., gt=1)
    quantity: int | None = Field(default=None, gt=0, lt=1000)
    weight_gram: float | None = Field(default=None, gt=0)
    @model_validator(mode="after")
    def quantityOrWeight(self):
        hasQuantity = self.quantity is not None
        hasWeight = self.weight_gram is not None
        if hasQuantity == hasWeight:
            raise HTTPException(status_code=400,
                                detail="One and only one out of quntity and weight must exist")
        return self    