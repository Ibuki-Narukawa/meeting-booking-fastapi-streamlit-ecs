from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


# Read(index)

# ユーザー一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()

# 会議室一覧取得
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Room).offset(skip).limit(limit).all()

# 予約一覧取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Booking).offset(skip).limit(limit).all()


# Read(show)

# 指定したuser_idのユーザーを取得
def get_user(db: Session, user_id: int):
  db_user =  db.query(models.User).filter(models.User.user_id == user_id).first()
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return db_user

# 指定したroom_idのユーザーを取得
def get_room(db: Session, room_id: int):
  db_room =  db.query(models.Room).filter(models.Room.room_id == room_id).first()
  if db_room is None:
    raise HTTPException(status_code=404, detail="Room not found")
  return db_room

# 指定したbooking_idのユーザーを取得
def get_booking(db: Session, booking_id: int):
  db_booking =  db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
  if db_booking is None:
    raise HTTPException(status_code=404, detail="Booking not found")
  return db_booking


# Create

# ユーザー登録
def create_user(db: Session, user: schemas.UserCreate):
  db_user = models.User(username=user.username)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

# 会議室登録
def create_room(db: Session, room: schemas.RoomCreate):
  db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
  db.add(db_room)
  db.commit()
  db.refresh(db_room)
  return db_room

# 予約登録
def create_booking(db: Session, booking: schemas.BookingCreate):
  db_booked = db.query(models.Booking).\
    filter(models.Booking.room_id == booking.room_id).\
    filter(models.Booking.end_datetime > booking.start_datetime).\
    filter(models.Booking.start_datetime < booking.end_datetime).\
    all()
   
  # 重複するデータがなければ
  if len(db_booked) == 0:
    db_booking = models.Booking(
      user_id = booking.user_id,
      room_id = booking.room_id,
      booked_num = booking.booked_num,
      start_datetime = booking.start_datetime,
      end_datetime = booking.end_datetime
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
  else:
    raise HTTPException(status_code=404, detail="Already booked")


# Update

# 指定したuser_idのユーザーを編集
def update_user(db: Session, user_id: int, user: schemas.UserCreate):
  db_user =  db.query(models.User).filter(models.User.user_id == user_id).first()
 
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  else:
    db_booked = db.query(models.User).\
    filter(models.User.username == user.username).\
    all()
  
    # 重複するデータがなければ
    if len(db_booked) == 0:
      db_user.username = user.username
      db.commit()
      db.refresh(db_user)
      return db_user
    else:
      raise HTTPException(status_code=404, detail="This name is already booked")


# 指定したroom_idの会議室を編集
def update_room(db: Session, room_id: int, room: schemas.RoomCreate):
  db_room =  db.query(models.Room).filter(models.Room.room_id == room_id).first()
 
  if db_room is None:
    raise HTTPException(status_code=404, detail="room not found")
  else:
    db_booked = db.query(models.Room).\
    filter(models.Room.room_name == room.room_name).\
    all()
  
    # 重複するデータがなければ
    if len(db_booked) == 0:
      db_room.room_name = room.room_name
      db_room.capacity = room.capacity
      db.commit()
      db.refresh(db_room)
      return db_room
    else:
      raise HTTPException(status_code=404, detail="This name is already booked")

# 指定したbooking_idの予約を編集
def update_booking(db: Session, booking_id: int, booking: schemas.BookingCreate):
  db_booking =  db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
 
  if db_booking is None:
    raise HTTPException(status_code=404, detail="booking not found")
  else:
    db_booked = db.query(models.Booking).\
    filter(models.Booking.room_id == booking.room_id).\
    filter(models.Booking.end_datetime > booking.start_datetime).\
    filter(models.Booking.start_datetime < booking.end_datetime).\
    all()
  
    # 重複するデータがなければ
    if len(db_booked) == 0:
      db_booking.user_id = booking.user_id
      db_booking.room_id = booking.room_id
      db_booking.booked_num = booking.booked_num
      db_booking.start_datetime = booking.start_datetime
      db_booking.end_datetime = booking.end_datetime
      db.commit()
      db.refresh(db_booking)
      return db_booking
    else:
      raise HTTPException(status_code=404, detail="Already booked")


# Delete

# 指定したuser_idのユーザーを削除
def delete_user(db: Session, user_id: int):
  db_user =  db.query(models.User).filter(models.User.user_id == user_id).first()
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  else:
    db_booked = db.query(models.Booking).\
    filter(models.Booking.user_id == db_user.user_id).\
    all()

    # 予約にこのユーザーが使われてなければ
    if len(db_booked) == 0:
      db.delete(db_user)
      db.commit()
      return {'message': 'success'}
    else:
      raise HTTPException(status_code=404, detail="This user is used at the time of booking")
  
# 指定したroom_idの会議室を削除
def delete_room(db: Session, room_id: int):
  db_room =  db.query(models.Room).filter(models.Room.room_id == room_id).first()
  if db_room is None:
    raise HTTPException(status_code=404, detail="room not found")
  else:
    db_booked = db.query(models.Booking).\
    filter(models.Booking.room_id == db_room.room_id).\
    all()

    # 予約にこの会議室が使われてなければ
    if len(db_booked) == 0:
      db.delete(db_room)
      db.commit()
      return {'message': 'success'}
    else:
      raise HTTPException(status_code=404, detail="This room is used at the time of booking")

# 指定したbooking_idの予約を削除
def delete_booking(db: Session, booking_id: int):
  db_booking =  db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
  if db_booking is None:
    raise HTTPException(status_code=404, detail="booking not found")
  else:
    db.delete(db_booking)
    db.commit()
    return {'message': 'success'}
