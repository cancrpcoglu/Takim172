from app.models.seller import Seller


class SellerService:

    @staticmethod
    def register_seller(db, user_id: int, store_name: str, description: str, rating: int):


        existing = db.query(Seller).filter(Seller.user_id == user_id).first()

        if existing:
          raise Exception("This user already has a seller account")
        if not user_id:
            raise Exception("User required")

        if not store_name:
            raise Exception("Store name required")

        seller = Seller(
            user_id=user_id,
            store_name=store_name,
            description=description,
            rating=rating,
            is_deleted=False
        )

        db.add(seller)
        db.commit()
        db.refresh(seller)

        return seller


    @staticmethod
    def get_sellers(db):
        return db.query(Seller).filter(Seller.is_deleted == False).all()


    @staticmethod
    def get_by_id(db, seller_id: int):
        return db.query(Seller).filter(
            Seller.id == seller_id,
            Seller.is_deleted == False
        ).first()


    @staticmethod
    def get_by_user(db, user_id: int):
        return db.query(Seller).filter(
            Seller.user_id == user_id,
            Seller.is_deleted == False
        ).first()


    @staticmethod
    def update_seller(db, seller_id: int, store_name: str, description: str, rating: int):

        seller = SellerService.get_by_id(db, seller_id)

        if not seller:
            return None

        seller.store_name = store_name
        seller.description = description
        seller.rating = rating

        db.commit()

        return seller


    @staticmethod
    def delete_seller(db, seller_id: int):

        seller = SellerService.get_by_id(db, seller_id)

        if not seller:
            return None

        seller.is_deleted = True
        db.commit()

        return seller