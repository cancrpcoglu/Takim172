from backend.app.models.order import Order
from backend.app.models.shipment import Shipment


class ShipmentService:

    @staticmethod
    def create_shipment(db, order_id: int, cargo_company: str, tracking_number: str = None):
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise Exception("Order not found")

        if not order_id:
            raise Exception("Order required")

        if not cargo_company:
            raise Exception("Cargo company required")
        existing = db.query(Shipment).filter(Shipment.order_id == order_id).first()

        if existing:
            raise Exception("Shipment already exists for this order")
        
        if order.status == "cancelled":
            raise Exception("Cancelled order cannot have shipment")

        shipment = Shipment(
            order_id=order_id,
            cargo_company=cargo_company,
            tracking_number=tracking_number,
            status="preparing",
            is_deleted=False
        )

        db.add(shipment)
        db.commit()
        db.refresh(shipment)

        return shipment


    @staticmethod
    def get_shipments(db):
        return db.query(Shipment).filter(Shipment.is_deleted == False).all()


    @staticmethod
    def get_by_id(db, shipment_id: int):
        return db.query(Shipment).filter(
            Shipment.id == shipment_id,
            Shipment.is_deleted == False
        ).first()


    @staticmethod
    def get_by_order(db, order_id: int):
        return db.query(Shipment).filter(
            Shipment.order_id == order_id,
            Shipment.is_deleted == False
        ).first()


    @staticmethod
    def update_status(db, shipment_id: int, status: str):

        shipment = ShipmentService.get_by_id(db, shipment_id)

        if not shipment:
            return None

        shipment.status = status
        db.commit()

        return shipment


    @staticmethod
    def update_tracking(db, shipment_id: int, tracking_number: str):

        shipment = ShipmentService.get_by_id(db, shipment_id)

        if not shipment:
            return None

        shipment.tracking_number = tracking_number
        db.commit()

        return shipment


    @staticmethod
    def delete_shipment(db, shipment_id: int):

        shipment = ShipmentService.get_by_id(db, shipment_id)

        if not shipment:
            return None

        shipment.is_deleted = True
        db.commit()

        return shipment