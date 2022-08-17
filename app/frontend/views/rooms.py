import os
from anyio import CapacityLimiter
from sqlalchemy import null
import streamlit as st
import json
import requests
import pandas as pd
from . import bookings

URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8080")

# FastAPIから会議室一覧を取得
def get_rooms():
  url_rooms = f'{URL}/rooms'
  res = requests.get(url_rooms)
  rooms = res.json()
  return rooms


# FastAPIから指定したIDの会議室を取得
def get_room(room_id: int):
  url = f'{URL}/rooms/{room_id}'
  res = requests.get(url)
  room = res.json()
  return room


# 会議室登録画面
def get_create_page():
  st.title('会議室登録画面')
  with st.form(key='room'):
    room_name: str = st.text_input('会議室名', max_chars=12)
    capacity: int = st.number_input('定員', step=1)
    data = {
      'room_name': room_name,
      'capacity': capacity
    }
    submit_button = st.form_submit_button(label = '会議室登録')

  if submit_button:
    st.write('## レスポンスデータ')
    url = f'{URL}/rooms'
    res = requests.post(
      url,
      json.dumps(data)
    )
    if res.status_code == 200:
      st.success('会議室登録完了')
    st.write(res.status_code)
    st.json(res.json())


# 会議室一覧表示
def get_index_page():
  rooms = get_rooms()
  if len(rooms) == 0:
    st.error('会議室が登録されていません。')
  else:
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)
    return rooms


# サイドバーからroom_idを入力する
def input_room_id():
  room_id = st.sidebar.number_input(label="room id:", min_value=1, step=1)
  get_room_button = st.sidebar.button("Get Room")

  if get_room_button:
    return room_id


# 会議室詳細ページ
def get_show_page(room_id):
  if room_id is None:
    st.write('## この中から会議室を選んでください')
    get_index_page()
  else:
    st.title('会議室詳細')
    room = get_room(room_id)
    st.json(room)


# 会議室編集ページ
def get_update_page():
  if "room_id" not in st.session_state or st.session_state['room_id'] == 0:
    rooms = get_rooms()
    rooms_name = bookings.make_rooms_name_dict(rooms)
    room_name: str = st.selectbox('編集したい会議室を選んでください', rooms_name.keys())
    get_room_button = st.button("Get room")

    if get_room_button:
      room_id = rooms_name[room_name]['room_id']
      st.session_state['room_id'] = room_id
      get_update_page()
      
  else:
    room_id = st.session_state['room_id']
    room = get_room(room_id)
    with st.form(key='update_room'):
      room_name: str = st.text_input('会議室名', value=room['room_name'], max_chars=12)
      capacity: int = st.number_input('定員', value=room['capacity'], min_value=1, step=1)
      data = {
        'room_name': room_name,
        'capacity': capacity
      }
      put_room_button = st.form_submit_button(label = '会議室編集')
    if put_room_button:
      st.write('## レスポンス結果')
      url = f'{URL}/rooms/{room_id}'
      res = requests.put(
        url,
        data=json.dumps(data)
      )
      if res.status_code == 200:
        st.success('会議室編集完了')
        st.session_state['room_id'] = 0
      st.write(res.status_code)
      st.json(res.json())
      st.session_state['room_id'] = 0
      reset_button = st.button('戻る')
      if reset_button:
        get_update_page()


# 会議室削除ページ
def get_delete_page():
  if "room_id" not in st.session_state or st.session_state['room_id'] == 0:
    rooms = get_rooms()
    rooms_name = bookings.make_rooms_name_dict(rooms)
    room_name: str = st.selectbox('削除したい会議室を選んでください', rooms_name.keys())
    get_room_button = st.button("Get room")

    if get_room_button:
      room_id = rooms_name[room_name]['room_id']
      st.session_state['room_id'] = room_id
      get_delete_page()

  else:
    room_id = st.session_state['room_id']
    room = get_room(room_id)
    st.write(room)
    delete_room_button = st.button("Delete room")

    if delete_room_button:
      st.write('## レスポンス結果')
      url = f'{URL}/rooms/{room_id}'
      res = requests.delete(url)
      if res.status_code == 200:
        st.success('会議室削除完了')
      else:
        st.write(res.status_code)
        st.json(res.json())
      st.session_state['room_id'] = 0
      reset_button = st.button('戻る')
      if reset_button:
        get_delete_page()
