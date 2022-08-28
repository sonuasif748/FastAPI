from sqlalchemy.orm import Session
import models
import schema


def get_address(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()

def get_address_by_id(db: Session, id: int):
    return db.query(models.Address).filter(models.Address.id == id).first()

def get_address_by_address_id(db: Session, coordinate: str):
    return db.query(models.Address).filter(models.Address.coordinate == coordinate).first()

def add_address_details_to_db(db: Session, address: schema.AddressBase):
    ad_details = models.Address(
        address=address.address,
        coordinate=address.coordinate,
    )
    db.add(ad_details)
    db.commit()
    db.refresh(ad_details)
    return models.Address(**address.dict())

def update_address_details(db: Session, id: int, details: schema.UpdateAddress):
    db.query(models.Address).filter(models.Address.id == id).update(vars(details))
    db.commit()
    return db.query(models.Address).filter(models.Address.id == id).first()

def delete_address_details_by_id(db: Session, id: int):

    try:
        db.query(models.Address).filter(models.Address.id == id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)