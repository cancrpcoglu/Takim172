from app.models.order import Order


class OrderService:

    @staticmethod
    def create_order(db, user_id: int, product_id: int, quantity: int):

        if not user_id:
            raise Exception("User required")

        if not product_id:
            raise Exception("Product required")

        if quantity <= 0:
            raise Exception("Quantity must be greater than 0")

        order = Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            status="pending",
            is_deleted=False
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        return order


    @staticmethod
    def get_orders(db):
        return db.query(Order).filter(Order.is_deleted == False).all()


    @staticmethod
    def get_my_orders(db, user_id: int):
        return db.query(Order).filter(
            Order.user_id == user_id,
            Order.is_deleted == False
        ).all()


    @staticmethod
    def get_by_id(db, order_id: int):
        return db.query(Order).filter(
            Order.id == order_id,
            Order.is_deleted == False
        ).first()


    @staticmethod
    def cancel_order(db, order_id: int):

        order = OrderService.get_by_id(db, order_id)

        if not order:
            return None

        order.status = "cancelled"
        db.commit()

        return order


    @staticmethod
    def update_status(db, order_id: int, status: str):

        order = OrderService.get_by_id(db, order_id)

        if not order:
            return None

        order.status = status
        db.commit()

        return order


    @staticmethod
    def delete_order(db, order_id: int):

        order = OrderService.get_by_id(db, order_id)

        if not order:
            return None

        order.is_deleted = True
        db.commit()

        return order