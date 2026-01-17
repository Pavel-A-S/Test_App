from pydantic import BaseModel, PositiveInt

class AddItemRequest(BaseModel):
    order_id: PositiveInt
    product_id: PositiveInt
    quantity: PositiveInt

class AddItemResponse(BaseModel):
    order_id: int
    product_id: int
    new_quantity: int