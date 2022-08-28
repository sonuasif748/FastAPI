from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schema
from database import SessionLocal, engine
from utils import distancefinder

models.Base.metadata.create_all(bind=engine)

# initiating app
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', response_model=List[schema.Addres])
def retrieve_all_address_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    address = crud.get_address(db=db, skip=skip, limit=limit)
    return address

@app.get('/distance')
def retrieve_distance_from_details(city:str, limit: int = 100, db: Session = Depends(get_db)):
    address = crud.get_address(db=db, skip=0, limit=limit)
    myloc = [i.coordinate for i in address if i.address == city][0].split(',')
    data = []
    for i in address:
        loc = i.coordinate.split(',')
        distance = distancefinder(myloc,loc)
        if city != i.address:
            data.append({f"{city} to {i.address}":f"{round(distance,2)} km"})
        else:
            pass
    return data

@app.post('/add', response_model=schema.AddressAdd)
def add_new_address(address: schema.AddressBase, db: Session = Depends(get_db)):
    address_id = crud.get_address_by_address_id(db=db, coordinate=address.coordinate)
    if address_id:
        raise HTTPException(status_code=400, detail=f"Address id {address.coordinate} already exist in database: {address_id}")
    return crud.add_address_details_to_db(db=db, address=address)


@app.delete('/delete/{id}')
def delete_address_by_id(id: int, db: Session = Depends(get_db)):
    details = crud.get_address_by_id(db=db, id=id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    try:
        crud.delete_address_details_by_id(db=db, id=id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return {"delete status": "success"}

@app.put('/update/{id}', response_model=schema.Addres)
def update_address_details(id: int, update_param: schema.UpdateAddress, db: Session = Depends(get_db)):
    details = crud.get_address_by_id(db=db, id=id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to update")
    return crud.update_address_details(db=db, details=update_param, id=id)