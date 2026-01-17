from fastapi import APIRouter, HTTPException
from app.models import AddItemRequest, AddItemResponse
from app.services.orders import add_or_update_item_in_order

router = APIRouter()

@router.post(
    "/add-item", response_model=AddItemResponse,
    responses={
        400: {
            "description": "Not enough quantity",
            "content": {
                "application/json": {
                    "example": {"detail": "Not enough quantity for this product"}
                }
            }
        },
        404: {
            "description": "Order not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Order does not exist"}
                }
            }
        },
        500: {"description": "Internal Server Error"},
    },
)
def add_item(req: AddItemRequest):
    try:
        return add_or_update_item_in_order(req.order_id, req.product_id, req.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))