from http.client import responses
import streamlit as st

import views

func = st.sidebar.radio(
  "Choose function",
  ('Create', 'Read(index)', 'Read(show)', 'Update', 'Delete')
)

page = st.sidebar.selectbox(
  'Choose your page',
  ['users', 'rooms', 'bookings'],
  2,
)


if func == 'Create':
  # ユーザー登録画面
  if page == 'users':
    views.users.get_create_page()

  # 会議室登録画面
  elif page == 'rooms':
    views.rooms.get_create_page()

  # 会議室予約画面
  elif page == 'bookings':
    views.bookings.get_create_page()

elif func == 'Read(index)':
  # ユーザー一覧
  if page == 'users':
    st.title('ユーザー一覧')
    views.users.get_index_page()

  # 会議室一覧
  elif page == 'rooms':
    st.title('会議室一覧')
    views.rooms.get_index_page()
  
  # 予約一覧
  elif page == 'bookings':
    st.title('予約一覧')
    views.bookings.get_index_page()

elif func == 'Read(show)':
  # ユーザー詳細
  if page == 'users':
    user_id = views.users.input_user_id()
    views.users.get_show_page(user_id)

  # 会議室詳細
  elif page == 'rooms':
    room_id = views.rooms.input_room_id()
    views.rooms.get_show_page(room_id)
  
  # 予約詳細
  elif page == 'bookings':
    booking_id = views.bookings.input_booking_id()
    views.bookings.get_show_page(booking_id)

elif func == 'Update':
  # ユーザー編集
  if page == 'users':
    st.title('ユーザー編集')
    views.users.get_update_page()

  # 会議室編集
  elif page == 'rooms':
    st.title('会議室編集')
    views.rooms.get_update_page()
  
  # 予約編集
  elif page == 'bookings':
    st.title('予約編集')
    views.bookings.get_update_page()

elif func == 'Delete':
  # ユーザー削除
  if page == 'users':
    st.title('ユーザー削除')
    views.users.get_delete_page()

  # 会議室削除
  elif page == 'rooms':
    st.title('会議室削除')
    views.rooms.get_delete_page()
  
  # 予約削除
  elif page == 'bookings':
    st.title('予約削除')
    views.bookings.get_delete_page()
