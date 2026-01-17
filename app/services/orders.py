from fastapi import HTTPException
from app.db import get_db_connection

def add_or_update_item_in_order(order_id: int, product_id: int, quantity: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM orders WHERE id=%s", (order_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Order does not exist")

            cursor.execute(
                """
                UPDATE products
                SET quantity = quantity - %s
                WHERE id = %s AND quantity >= %s
                """,
                (quantity, product_id, quantity)
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=400, detail="Not enough quantity for this product")

            cursor.execute(
                """
                INSERT INTO order_items (order_id, product_id, quantity)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
                """,
                (order_id, product_id, quantity)
            )

            conn.commit()

            cursor.execute(
                "SELECT quantity FROM order_items WHERE order_id=%s AND product_id=%s",
                (order_id, product_id)
            )
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(status_code=500, detail="Failed to fetch updated order item")

            new_quantity = row["quantity"]

        return {"order_id": order_id, "product_id": product_id, "new_quantity": new_quantity}

    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()