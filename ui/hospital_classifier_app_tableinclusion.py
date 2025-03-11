import sqlite3
from typing import Optional

import requests
import streamlit as st
from app.settings import API_BASE_URL  # Assuming you have this settings file
from PIL import Image
import random

ST_NEW_USER = "new_user"
ST_REGISTER = "register"
ST_TOKEN = "token"
ST_RESTART = "restart"

def get_payload(fields: dict):
    payload = {}
    with_error = False

    for field in fields:
        if field["type"] == "float" or field["type"] == "int":
            min_val = field["min"]
            max_val = field["max"]

            value = st.text_input(field["name"])
            st.markdown(f"Enter a number between {min_val} and {max_val}")

            if value:
                try:
                    number = float(value)
                    if min_val <= number <= max_val:
                        st.success("Valid input: {}".format(number))
                    else:
                        st.error("Please enter a number between {} and {}.".format(min_val, max_val))
                        with_error = True

                except ValueError:
                    st.error("Please enter a valid number.")
                    with_error = True

            else:
                with_error = True

        elif field["type"] == "options":
            value = st.selectbox(field["name"], field["options"])

        payload[field["id"]] = value

    return payload, with_error

def register(username: str, password: str, name: str) -> Optional[str]:
    url = f"{API_BASE_URL}/user"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "grant_type": "",
        "username": username,
        "password": password,
        "name": name,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            INSERT INTO users (username, password, name)
            VALUES (?, ?, ?)
        ''', (username, password, name))

        conn.commit()
        conn.close()

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            token = login(username, password)
        else:
            token = None

        return token

    except sqlite3.Error as e:
        st.error(f"Error saving user to database: {e}")
        return None

def login(username: str, password: str) -> Optional[str]:
    url = f"{API_BASE_URL}/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        token = response.json()["access_token"]
    else:
        token = None

    return token

def m_predict(token: str, form_data: dict):
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data

        def json(self):
            return self._json_data

    score = random.random()

    mock_result = {
        "prediction": "You are in fire!" if score > 0.5 else "No insurance need..",
        "score": score,
    }

    st.write(f"**Payload:** {form_data}")

    return MockResponse(status_code=200, json_data=mock_result)

def predict(token: str, form_data: dict) -> requests.Response:
    headers = {"Authorization": f"Bearer {token}"}

    return {
        "status_code": 200,
    }

    url = f"{API_BASE_URL}/model/predict"
    response = requests.post(url, headers=headers, data=form_data)

    return response

def check_state(state: str, remove: bool = False):
    if state in st.session_state:
        value = st.session_state[state]
        if remove:
            del st.session_state[state]
        return value

    return False

st.set_page_config(page_title="Hospitalization Risks", page_icon="✈️")

st.markdown(
    "<h1 style='text-align: center; color: #4B89DC;'>Hospitalization Risks</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
        .st-key-new_user > .stButton > button {
            background: none !important;
            border: none !important;
            color: blue !important;
            text-decoration: none !important;
            cursor: pointer !important;
            font-size: 16px !important;
            padding: 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if check_state(ST_RESTART):
    check_state(ST_TOKEN, True)
    check_state(ST_NEW_USER, True)

placeholder = st.empty()

with placeholder.container():
    if not check_state(ST_TOKEN):
        label = "Login" if ST_NEW_USER not in st.session_state else "Register"

        st.markdown(f"## {label}")
        email = st.text_input("E-Mail")
        password = st.text_input("Password", type="password")

        token = None
        if check_state(ST_NEW_USER):
            name = st.text_input("Name")
            st.session_state[ST_NEW_USER] = True

            if st.button("Register"):
                token = register(email, password, name)

        else:
            col1, col2 = st.columns([1, 5])

            with col1:
                if st.button("Login"):
                    token = login(email, password)
                    print("Paso por token")

            with col2:
                if st.button("I haven't had the pleasure of registering yet!", key=ST_NEW_USER):
                    pass

        if token is None:
            pass

        elif token:
            st.session_state.email = email if email > "" else "No name"
            st.session_state.token = token
            st.success(f"{label} successful!")

        else:
            st.error(f"{label} failed. Please try again.")

        st.html("</span>")

if ST_TOKEN in st.session_state:
    placeholder.empty()
    st.success(f"{st.session_state.email}, you are logged in!")

    token = st.session_state.token

    st.markdown("## Prediction Form")

    fields = [
        {"id": "glucosa", "name": "Glucosa", "type": "float", "min": 0, "max": 500},
        {"id": "hemoglobina", "name": "Hemoglobina", "type": "options", "options": ["Si", "No"]},
    ]

    payload, with_error = get_payload(fields)

    col1, col2 = st.columns([1, 5])

    response = False
    with col1:
        if st.button("Predict"):
            if with_error:
                pass

            else:
                response = m_predict(token, payload)

        else:
            with_error = False

    with col2:
        if st.button("Re-start", key=ST_RESTART):
            pass

    if response:
        if response.status_code == 200:
            result = response.json()
            st.write(f"**Prediction:** {result['prediction']}")
            st.write(f"**Score:** {format(result['score'], '.2f')}") 
            st.session_state.classification_done = True
            st.session_state.result = result
        else:
            st.error(f"Error predicting data. Please try again. ({response.status_code})")


    elif with_error:
        st.error("Please correct the errors before predicting.")


    # Pie de página
    st.markdown("<hr style='border:2px solid #4B89DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #4B89DC;'>2025 Hospitalization predict App</p>",
        unsafe_allow_html=True,
    )