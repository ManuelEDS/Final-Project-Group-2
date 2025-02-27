from typing import Optional

import requests
import streamlit as st
from app.settings import API_BASE_URL
from PIL import Image
import random


def register(username: str, password: str) -> Optional[str]:
    """This function calls the register endpoint of the API to create a new user.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if registration is successful, None otherwise
    """

    # Steps to Build the `register` Function:
    #  1. Construct the API endpoint URL using `API_BASE_URL` and `/register`.
    url = f"{API_BASE_URL}/register"

    #  2. Set up the request headers with `accept: application/json` and
    #     `Content-Type: application/x-www-form-urlencoded`.
    headers = { 
        "accept" : "application/json",
        "Content-Type" : "application/x-www-form-urlencoded" 
    }

    #  3. Prepare the data payload with fields: `grant_type`, `username`, `password`,
    #     `scope`, `client_id`, and `client_secret`.
    payload = { 
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    #  4. Use `requests.post()` to send the API request with the URL, headers,
    #     and data payload.

    random_number = random.random()
    return random_number>.5

    # TODO: Check the register API (MD) 
    response = requests.post(url, headers=headers, data=payload)

    #  5. Check if the response status code is `200`.
    #  6. If successful, extract the token from the JSON response.
    #  7. Return the token if login is successful, otherwise return `None`.
    #  8. Test the function with various inputs.
    if response.status_code == 200:
        token = response.json()["access_token"]
        st.success(f"Register successful!")
    else:
        token = None

    return token

def login(username: str, password: str) -> Optional[str]:
    """This function calls the login endpoint of the API to authenticate the user
    and get a token.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if login is successful, None otherwise
    """
    # Steps to Build the `login` Function:
    #  1. Construct the API endpoint URL using `API_BASE_URL` and `/login`.
    url = f"{API_BASE_URL}/login"

    #  2. Set up the request headers with `accept: application/json` and
    #     `Content-Type: application/x-www-form-urlencoded`.
    headers = { 
        "accept" : "application/json",
        "Content-Type" : "application/x-www-form-urlencoded" 
    }

    #  3. Prepare the data payload with fields: `grant_type`, `username`, `password`,
    #     `scope`, `client_id`, and `client_secret`.
    payload = { 
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    #  4. Use `requests.post()` to send the API request with the URL, headers,
    #     and data payload.

    random_number = random.random()
    return random_number>.5

    # TODO: Check the login API (MD) 
    response = requests.post(url, headers=headers, data=payload)

    #  5. Check if the response status code is `200`.
    #  6. If successful, extract the token from the JSON response.
    #  7. Return the token if login is successful, otherwise return `None`.
    #  8. Test the function with various inputs.
    if response.status_code == 200:
        token = response.json()["access_token"]
        st.success(f"Log in successful!")
    else:
        token = None
        #st.error(f"Error: {response.json()}")

    return token

def m_predict(token: str, form_data: dict):

    # Simular la respuesta de la API
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data

        def json(self):
            return self._json_data

    # Datos simulados de la API
    mock_result = {
        "prediction": "Positive",
        "score": random.random()
    }

    st.write(f"**Payload:** {form_data}")
    
    
    return MockResponse(status_code=200 if random.random()>.3 else 400, json_data=mock_result)

def predict(token: str, form_data: dict) -> requests.Response:
    """This function calls the predict endpoint of the API to classify the uploaded
    image.

    Args:
        token (str): token to authenticate the user
        uploaded_file (Image): image to classify

    Returns:
        requests.Response: response from the API
    """

    # Steps to Build the `predict` Function:
    #  1. Create a dictionary with the file data. The file should be a
    #     tuple with the file name and the file content.

    #  2. Add the token to the headers.
    headers = {"Authorization": f"Bearer {token}"}

    #  3. Make a POST request to the predict endpoint.

    return {
        "status_code" : 200,
    }

    # TODO: Check the predict API (MD) 
    url = f"{API_BASE_URL}/model/predict"
    response = requests.post(url, headers=headers, data=form_data)

    #  4. Return the response.
    return response


# Interfaz de usuario
#st.set_page_config(page_title="Hospitalization Risks", page_icon="📷🏥")
st.set_page_config(page_title="Hospitalization Risks", page_icon="✈️")


st.markdown(
    "<h1 style='text-align: center; color: #4B89DC;'>Hospitalization Risks</h1>",
    unsafe_allow_html=True,
)

# Formulario de login/register
if "token" not in st.session_state:
    st.markdown("## Login")
    username = st.text_input("Username", value="alejandro.miconi@gmail.com")
    password = st.text_input("Password", type="password", value="admin")


    # Crear dos columnas
    col1, col2 = st.columns(2)

    with col1:

        if st.button("Login"):
            token = login(username, password)
            if token:
                st.session_state.token = token
                st.success("Login successful!")
            else:
                st.error("Login failed. Please check your credentials.")


    with col2:

        if st.button("Register"):
            token = register(username, password)
            if token:
                st.session_state.token = token
                st.success("Register successful!")
            else:
                st.error("Register failed. Please check your credentials.")



else:
    st.success("You are logged in!")


if "token" in st.session_state:
    token = st.session_state.token

    # TODO: Add the form to inputs (GF)
    f_glucosa = st.text_input("Glucosa")
    f_hemoglobina = st.text_input("Hemoglobina")

    # Predict button
    if st.button("Predict"):

        payload = {
            "glucosa": f_glucosa, 
            "hemoglobina": f_hemoglobina
        }

        response = m_predict(token, payload)

        if response.status_code == 200:
            result = response.json()
            st.write(f"**Prediction:** {result['prediction']}") 
            st.write(f"**Score:** {format(result['score'], '.2f')}") 
            #st.write(f"**Score:** {result['score']}")
            st.session_state.classification_done = True
            st.session_state.result = result
        else:
            st.error(f"Error predicting data. Please try again. ({response.status_code})")

    # Pie de página
    st.markdown("<hr style='border:2px solid #4B89DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #4B89DC;'>2025 Hospitalization predict App</p>",
        unsafe_allow_html=True,
    )
