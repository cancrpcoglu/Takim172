from app.models.product import Product


class ProductService:

    @staticmethod
    def create_product(db, seller_id: int, data: dict):

        if not seller_id:
            raise Exception("Seller required")

        name = data.get("name")
        price = data.get("price")
        stock = data.get("stock", 0)

        if not name:
            raise Exception("Product name required")

        if price is None or price <= 0:
            raise Exception("Invalid price")

        if stock < 0:
            raise Exception("Invalid stock value")

        product = Product(
            seller_id=seller_id,
            name=name,
            price=price,
            stock=stock,
            is_deleted=False
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product