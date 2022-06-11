import os
import streamlit as st
import json
import requests
import datetime
import pandas as pd
from . import users, rooms

URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8080")

# FastAPIから予約一覧を取得
def get_bookings():
  url_bookings = f'{URL}/bookings'
  res = requests.get(url_bookings)
  bookings = res.json()
  return bookings


# FastAPIから指定したIDの予約を取得
def get_booking(booking_id: int):
  url = f'{URL}/bookings/{booking_id}'
  res = requests.get(url)
  booking = res.json()
  return booking


# usernameからuser_idを参照する辞書を作成
def make_users_name_dict(my_users):
  users_name = {}
  for user in my_users:
    users_name[user['username']] = user['user_id']
  return users_name

# room_nameからroom_idを参照する辞書を作成
def make_rooms_name_dict(my_rooms):
  rooms_name = {}
  for room in my_rooms:
    rooms_name[room['room_name']] = {
      'room_id': room['room_id'],
      'capacity': room['capacity']
    }
  return rooms_name

# user_idからusernameを参照する辞書を作成
def make_users_id_dict(my_users):
  users_id = {}
  for user in my_users:
    users_id[user['user_id']] = user['username']
  return users_id

# room_idからroom_nameを参照する辞書を作成
def make_rooms_id_dict(my_rooms):
  rooms_id = {}
  for room in my_rooms:
    rooms_id[room['room_id']] = {
      'room_name': room['room_name'],
      'capacity': room['capacity']
    }
  return rooms_id


# booking_idから予約情報を参照する辞書を作成
def make_bookings_id_dict(my_bookings):
  bookings_id = {}
  for booking in my_bookings:
    bookings_id[booking['booking_id']] = {
      'user_id': booking['user_id'],
      'room_id': booking['room_id'],
      'booked_num': booking['booked_num'],
      'start_datetime': booking['start_datetime'],
      'end_datetime': booking['end_datetime'],
    }
  return bookings_id


# 会議室予約画面
def get_create_page():
  st.title('会議室予約画面')

  # ユーザー一覧の取得
  my_users = users.get_users()
  if len(my_users) == 0:
    st.error('ユーザーが登録されていません。')
  else:
    # name->idを参照する辞書
    users_name = make_users_name_dict(my_users)
    # id->nameを参照する辞書
    users_id = make_users_id_dict(my_users)
  
  # 会議室一覧の取得
  st.write('### 会議室一覧')
  my_rooms = rooms.get_rooms()
  if len(my_rooms) == 0:
    st.error('会議室が登録されていません。')
  else:
    rooms_name = make_rooms_name_dict(my_rooms)
    rooms_id = make_rooms_id_dict(my_rooms)
    rooms.get_index_page()

  # 予約一覧の取得
  st.write('### 予約一覧')
  bookings = get_bookings()
  df_bookings = pd.DataFrame(bookings)
  if len(bookings) == 0:
    st.error('予約はありません。')
  else:
     # IDを各値に変更する関数
    to_username = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]['room_name']
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')

    # 特定の列に適用
    df_bookings['user_id'] = df_bookings['user_id'].map(to_username)
    df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
    df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
    df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)

    df_bookings = df_bookings.rename(columns={
      'user_id': '予約者名',
      'room_id': '会議室名',
      'booked_num': '予約人数',
      'start_datetime': '開始時刻',
      'end_datetime': '終了時刻',
      'booking_id': '予約番号'
    })

    st.table(df_bookings)
  
  if len(my_users) != 0 and len(my_rooms) != 0:
    with st.form(key='booking'):
      username: str = st.selectbox('予約者名', users_name.keys())
      room_name: str = st.selectbox('会議室名', rooms_name.keys())
      booked_num: int = st.number_input('予約人数', step=1, min_value=1)
      date: datetime.date = st.date_input('日付: ', min_value=datetime.date.today())
      start_time: datetime.time = st.time_input('開始時刻: ', value=datetime.time(hour=9, minute=0))
      end_time: datetime.time = st.time_input('終了時刻: ', value=datetime.time(hour=20, minute=0))
    
      submit_button = st.form_submit_button(label = '予約登録')

    if submit_button:
      user_id: int = users_name[username]
      room_id: int = rooms_name[room_name]['room_id']
      capacity: int = rooms_name[room_name]['capacity']

      data = {
      'user_id': user_id,
      'room_id': room_id,
      'booked_num': booked_num,
      'start_datetime': datetime.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=start_time.hour,
        minute=start_time.minute
      ).isoformat(),
      'end_datetime': datetime.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=end_time.hour,
        minute=end_time.minute
      ).isoformat()
      }

      # 定員より多いの予約人数の場合
      if booked_num > capacity:
        st.error(f'{room_name}の定員は、{capacity}名です。{capacity}名以下の予約人数のみ受け付けております。')
      
      # 開始時刻 >= 終了時刻の場合
      elif start_time >= end_time:
        st.error('開始時刻が終了時刻を超えています。')
      
      elif start_time < datetime.time(hour=9, minute=0, second=0) or end_time > datetime.time(hour=20, minute=0, second=0):
        st.error('利用時間は9:00~20:00になります。')

      else:
        url = f'{URL}/bookings'
        res = requests.post(
          url,
          data=json.dumps(data)
        )
        if res.status_code == 200:
          st.success('予約完了しました')
        elif res.status_code == 404 and res.json()['detail'] == 'Already booked':
          st.error('指定の時間には既に予約が入っています。')


 # 予約一覧表示
def get_index_page():
  
  # ユーザー一覧の取得
  my_users = users.get_users()
  if len(my_users) == 0:
    st.error('ユーザーが登録されていません。')
  else:
    # name->idを参照する辞書
    users_name = make_users_name_dict(my_users)
    # id->nameを参照する辞書
    users_id = make_users_id_dict(my_users)
  
  # 会議室一覧の取得
  my_rooms = rooms.get_rooms()
  if len(my_rooms) == 0:
    st.error('会議室が登録されていません。')
  else:
    rooms_name = make_rooms_name_dict(my_rooms)
    rooms_id = make_rooms_id_dict(my_rooms)

  # 予約一覧の取得
  bookings = get_bookings()
  df_bookings = pd.DataFrame(bookings)
  if len(bookings) == 0:
    st.error('予約はありません。')
  else:
     # IDを各値に変更する関数
    to_username = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]['room_name']
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')

    # 特定の列に適用
    df_bookings['user_id'] = df_bookings['user_id'].map(to_username)
    df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
    df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
    df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)

    df_bookings = df_bookings.rename(columns={
      'user_id': '予約者名',
      'room_id': '会議室名',
      'booked_num': '予約人数',
      'start_datetime': '開始時刻',
      'end_datetime': '終了時刻',
      'booking_id': '予約番号'
    })

    st.table(df_bookings)


# サイドバーからbooking_idを入力する
def input_booking_id():
  booking_id = st.sidebar.number_input(label="booking id:", min_value=1, step=1)
  get_booking_button = st.sidebar.button("Get Booking")

  if get_booking_button:
    return booking_id


# 会議室詳細ページ
def get_show_page(booking_id):
  if booking_id is None:
    st.write('## この中から予約を選んでください')
    get_index_page()
  else:
    st.title('予約詳細')
    booking = get_booking(booking_id)
    st.json(booking)


# 予約編集ページ
def get_update_page():
  if "booking_id" not in st.session_state or st.session_state['booking_id'] == 0:
    bookings = get_bookings()
    bookings_id = make_bookings_id_dict(bookings)
    st.write('## 編集したい予約を選んでください')
    get_index_page()
    booking_id: int = st.selectbox('予約ID', bookings_id.keys())
    get_booking_button = st.button("Get booking")

    if get_booking_button:
      st.session_state['booking_id'] = booking_id
      st.session_state['bookings_id'] = bookings_id
      get_update_page()
      
  else:
    booking_id = st.session_state['booking_id']
    bookings_id = st.session_state['bookings_id']
    booking = get_booking(booking_id)

    my_users = users.get_users()
    users_name = make_users_name_dict(my_users)

    my_rooms = rooms.get_rooms()
    rooms_name = make_rooms_name_dict(my_rooms)

    to_datetime = lambda x: datetime.datetime.fromisoformat(x)
    start_datetime = to_datetime(bookings_id[booking_id]['start_datetime'])
    end_datetime = to_datetime(bookings_id[booking_id]['end_datetime'])

    with st.form(key='update_booking'):
      username: str = st.selectbox('予約名', index=booking['booking_id']-1, options=users_name.keys())
      room_name: str = st.selectbox('会議室名', index=booking['room_id']-1, options=rooms_name.keys())
      booked_num: int = st.number_input('予約人数', step=1, min_value=1, value=bookings_id[booking_id]['booked_num'])
      date: datetime.date = st.date_input('日付: ', value=start_datetime)
      start_time: datetime.time = st.time_input('開始時刻: ', value=start_datetime)
      end_time: datetime.time = st.time_input('終了時刻: ', value=end_datetime)
  
      put_booking_button = st.form_submit_button(label = '予約編集')

    if put_booking_button:
      capacity: int = rooms_name[room_name]['capacity']
      data = {
        'user_id': users_name[username],
        'room_id': rooms_name[room_name]['room_id'],
        'booked_num': booked_num,
        'start_datetime': datetime.datetime(
          year=date.year,
          month=date.month,
          day=date.day,
          hour=start_time.hour,
          minute=start_time.minute
        ).isoformat(),
        'end_datetime': datetime.datetime(
          year=date.year,
          month=date.month,
          day=date.day,
          hour=end_time.hour,
          minute=end_time.minute
        ).isoformat()
      }

       # 定員より多いの予約人数の場合
      if booked_num > capacity:
        st.error(f'{room_name}の定員は、{capacity}名です。{capacity}名以下の予約人数のみ受け付けております。')
      
      # 開始時刻 >= 終了時刻の場合
      elif start_time >= end_time:
        st.error('開始時刻が終了時刻を超えています。')
      
      # 開始時刻 < 今日の日付の場合
      elif date < datetime.date.today():
        st.error('開始時刻は今日の日付以降にしてください。')
    
      elif start_time < datetime.time(hour=9, minute=0, second=0) or end_time > datetime.time(hour=20, minute=0, second=0):
        st.error('利用時間は9:00~20:00になります。')

      else:
        st.write('## レスポンス結果')
        url = f'{URL}/bookings/{booking_id}'
        res = requests.put(
          url,
          data=json.dumps(data)
        )
        if res.status_code == 200:
          st.success('予約編集完了')
          st.session_state['booking_id'] = 0
        st.write(res.status_code)
        st.json(res.json())
      st.session_state['booking_id'] = 0
      reset_button = st.button('戻る')
      if reset_button:
        get_update_page()


# 予約削除ページ
def get_delete_page():
  if "booking_id" not in st.session_state or st.session_state['booking_id'] == 0:
    bookings = get_bookings()
    bookings_id = make_bookings_id_dict(bookings)
    st.write('## 削除したい予約を選んでください')
    get_index_page()
    booking_id: int = st.selectbox('予約ID', bookings_id.keys())
    get_booking_button = st.button("Get booking")

    if get_booking_button:
      st.session_state['booking_id'] = booking_id
      st.session_state['bookings_id'] = bookings_id
      get_delete_page()
      
  else:
    booking_id = st.session_state['booking_id']
    booking = get_booking(booking_id)
    st.write(booking)
    delete_booking_button = st.button("Delete booking")

    if delete_booking_button:
      st.write('## レスポンス結果')
      url = f'{URL}/bookings/{booking_id}'
      res = requests.delete(url)
      if res.status_code == 200:
        st.success('予約削除完了')
      else:
        st.write(res.status_code)
        st.json(res.json())
      st.session_state['booking_id'] = 0
      reset_button = st.button('戻る')
      if reset_button:
        get_delete_page()
