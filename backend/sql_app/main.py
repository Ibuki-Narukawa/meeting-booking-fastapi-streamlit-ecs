from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# @app.get("/")
# async def index():
#   return {"message": "Success"}

# Healthcheck
@app.get("/healthcheck")
async def healthcheck():
  return "I'm healthy!"

# Read (index)
@app.get("/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  users = crud.get_users(db=db, skip=skip, limit=limit)
  return users

@app.get("/rooms", response_model=List[schemas.Room])
async def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  rooms = crud.get_rooms(db=db, skip=skip, limit=limit)
  return rooms

@app.get("/bookings", response_model=List[schemas.Booking])
async def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  bookings = crud.get_bookings(db=db, skip=skip, limit=limit)
  return bookings

# Read (show)
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
  return crud.get_user(db=db, user_id=user_id)

@app.get("/rooms/{room_id}", response_model=schemas.Room)
def read_room(room_id: int, db: Session = Depends(get_db)):
  return crud.get_room(db=db, room_id=room_id)

@app.get("/bookings/{booking_id}", response_model=schemas.Booking)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
  return crud.get_booking(db=db, booking_id=booking_id)


# Create
@app.post("/users")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.create_user(db=db, user=user)
  return db_user

@app.post("/rooms", response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
  db_room = crud.create_room(db=db, room=room)
  return db_room

@app.post("/bookings", response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
  db_booking = crud.create_booking(db=db, booking=booking)
  return db_booking


# Update
@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserCreate, db:Session = Depends(get_db)):
  return crud.update_user(db=db, user_id=user_id, user=user)

@app.put("/rooms/{room_id}", response_model=schemas.Room)
async def update_room(room_id: int, room: schemas.RoomCreate, db:Session = Depends(get_db)):
  return crud.update_room(db=db, room_id=room_id, room=room)

@app.put("/bookings/{booking_id}", response_model=schemas.Booking)
async def update_booking(booking_id: int, booking: schemas.BookingCreate, db:Session = Depends(get_db)):
  return crud.update_booking(db=db, booking_id=booking_id, booking=booking)


# Delete
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
  return crud.delete_user(db=db, user_id=user_id)

@app.delete("/rooms/{room_id}")
async def delete_room(room_id: int, db: Session = Depends(get_db)):
  return crud.delete_room(db=db, room_id=room_id)

@app.delete("/bookings/{booking_id}")
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
  return crud.delete_booking(db=db, booking_id=booking_id)
