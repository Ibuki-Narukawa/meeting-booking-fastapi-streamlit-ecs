import os
from turtle import onclick
from typing import Dict, List
from matplotlib.pyplot import get
from sqlalchemy import false, true
from . import bookings
from requests import session
from h11 import Data
import streamlit as st
import json
import requests
import pandas as pd

URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8080")

# FastAPIからユーザー一覧を取得
def get_users():
  url_users = f'{URL}/users'
  res = requests.get(url_users)
  users = res.json()
  return users

# FastAPIから指定したIDのユーザーを取得
def get_user(user_id: int):
  url = f'{URL}/users/{user_id}'
  res = requests.get(url)
  user = res.json()
  return user


# ユーザー登録画面
def get_create_page():
  st.title('ユーザー登録画面')

  with st.form(key='user'):
    username: str = st.text_input('ユーザー名', max_chars=12)
    data = {
      'username': username
    }
    submit_button = st.form_submit_button(label = 'ユーザー登録')

  if submit_button:
    st.write('## レスポンス結果')
    url = f'{URL}/users'
    res = requests.post(
      url,
      data=json.dumps(data)
    )
    if res.status_code == 200:
      st.success('ユーザー登録完了')
    st.write(res.status_code)
    st.json(res.json())


# ユーザー一覧表示
def get_index_page():
  users = get_users()
  if len(users) == 0:
    st.error('ユーザーが登録されていません。')
  else:
    df_users = pd.DataFrame(users)
    df_users.columns = ['ユーザー名', 'ユーザーID']
    st.table(df_users)


# サイドバーからuser_idを入力する
def input_user_id():
  with st.form(key='input_user_id'):
    with st.sidebar:
      user_id = st.sidebar.number_input(label="user id:", min_value=1, step=1)
      get_user_button = st.form_submit_button("Get User")

    if get_user_button:
      return user_id


# ユーザー詳細ページ
def get_show_page(user_id):
  if user_id is None:
    st.write('## この中からユーザーを選んでください')
    get_index_page()
  else:
    st.title('ユーザー詳細')
    user = get_user(user_id)
    st.json(user)


# ユーザー編集ページ
def get_update_page():
  if "user_id" not in st.session_state or st.session_state['user_id'] == 0:
    users = get_users()
    users_name = bookings.make_users_name_dict(users)
    username: str = st.selectbox('編集したいユーザーを選んでください', users_name.keys())
    get_user_button = st.button("Get User")

    if get_user_button:
      user_id = users_name[username]
      st.session_state['user_id'] = user_id
      get_update_page()
      
  else:
    user_id = st.session_state['user_id']
    user = get_user(user_id)
    with st.form(key='update_user'):
      username: str = st.text_input('ユーザー名', value=user['username'], max_chars=12)
      data = {
        'username': username
      }
      put_user_button = st.form_submit_button(label = 'ユーザー編集')
    if put_user_button:
      st.write('## レスポンス結果')
      url = f'{URL}/users/{user_id}'
      res = requests.put(
        url,
        data=json.dumps(data)
      )
      if res.status_code == 200:
        st.success('ユーザー編集完了')
        st.session_state['user_id'] = 0
      st.write(res.status_code)
      st.json(res.json())
      st.session_state['user_id'] = 0
      reset_button = st.button('戻る')
      if reset_button:
        get_update_page()


# ユーザー削除ページ
def get_delete_page():
  if "user_id" not in st.session_state or st.session_state['user_id'] == 0:
    users = get_users()
    users_name = bookings.make_users_name_dict(users)
    username: str = st.selectbox('削除したいユーザーを選んでください', users_name.keys())
    get_user_button = st.button("Get User")

    if get_user_button:
      user_id = users_name[username]
      st.session_state['user_id'] = user_id
      get_delete_page()

  else:
    user_id = st.session_state['user_id']
    user = get_user(user_id)
    st.write(user)
    delete_user_button = st.button("Delete User")

    if delete_user_button:
      st.write('## レスポンス結果')
      url = f'{URL}/users/{user_id}'
      res = requests.delete(url)
      if res.status_code == 200:
        st.success('ユーザー削除完了')
      else:
        st.write(res.status_code)
        st.json(res.json())

      st.session_state['user_id'] = 0
      reset_button = st.button('戻る')
      if reset_button:
        get_delete_page()
