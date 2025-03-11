from typing import Optional

import requests
import streamlit as st
from app.settings import API_BASE_URL
from PIL import Image
import random

ST_NEW_USER = "new_user"
ST_REGISTER = "register"
ST_TOKEN = "token"
ST_RESTART = "restart"
ST_PREDICT = "predict"
ST_FIRST = "first"

def register(username: str, password: str, name: str) -> Optional[str]:
    """This function calls the register endpoint of the API to create a new user.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if registration is successful, None otherwise
    """

    # Steps to Build the `register` Function:
    #  1. Construct the API endpoint URL using `API_BASE_URL` and `/register`.
    url = f"{API_BASE_URL}/user"

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
        "name": name,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    #  4. Use `requests.post()` to send the API request with the URL, headers,
    #     and data payload.

    return True

    # TODO: Check the register API (MD) 
    response = requests.post(url, headers=headers, data=payload)

    #  5. Check if the response status code is `200`.
    #  6. If successful, go login and extract the token from the JSON response.
    if response.status_code == 200:
        token = login(username, password)
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

    return True 

    # TODO: Check the login API (MD) 
    response = requests.post(url, headers=headers, data=payload)

    #  5. Check if the response status code is `200`.
    #  6. If successful, extract the token from the JSON response.
    #  7. Return the token if login is successful, otherwise return `None`.
    #  8. Test the function with various inputs.
    if response.status_code == 200:
        token = response.json()["access_token"]
    else:
        token = None

    return token

def m_predict(token: str, form_data: dict):

    # Simular la respuesta de la API
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data

        def json(self):
            return self._json_data


    score = random.random()

    # Datos simulados de la API
    mock_result = {
        "prediction": "You are in fire!" if score>.5 else "No insurance need..",
        "score": score
    }

    return MockResponse(status_code=200, json_data=mock_result)

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

def check_state(state: str, remove: bool = False):

    if state in st.session_state:
        value = st.session_state[state]
        if remove: del st.session_state[state]
        return value 

    return False

def get_payload(fields: dict):

    payload = {}
    with_error = False

    for field in fields:

        if field["type"] == "float" or field["type"] == "int":
        
            min = field["min"]
            max = field["max"]

            value = st.text_input(field["name"])
            st.markdown(f"""
                <span style="color: #4B89DC; font-size: smaller;">
                Enter a number between {min} and {max}
                </span>""", unsafe_allow_html=True)

            if value:
                try:
                    number = float(value)  # Convert input to a number
                    
                    if field["type"] == "int" and not number.is_integer():
                        st.error("Please enter a whole number.")
                        with_error = True                        
                    
                    elif not (min <= number <= max):
                        st.error("Please enter a number between {} and {}.".format(min, max))
                        with_error = True

                except ValueError:
                    st.error("Please enter a valid number.")

            else:
                #st.error("Please enter a valid value.")
                with_error = True

        elif field["type"] == "options":
            value = st.selectbox(field["name"], field["options"])

        payload[field["id"]] = value

    return payload , with_error



# Interfaz de usuario
#st.set_page_config(page_title="Hospitalization Risks", page_icon="📷🏥")
st.set_page_config(page_title="Hospitalization Risks", page_icon="✈️")


st.markdown(
    "<h1 style='text-align: center; color: #4B89DC;'>Hospitalization Risks</h1>",
    unsafe_allow_html=True,
)

# Custom CSS to style the button like a link
st.markdown("""
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
    unsafe_allow_html=True)


print("State", st.session_state)

if check_state(ST_RESTART):
    check_state(ST_TOKEN, True)
    check_state(ST_NEW_USER, True)
    check_state(ST_PREDICT, True)
    check_state(ST_FIRST, True)


# Create a placeholder
placeholder = st.empty()

with placeholder.container():

    # Login form
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
                            
            with col2:

                if st.button("I haven't had the pleasure of registering yet!", key=ST_NEW_USER):
                    pass

        if token == None:
            pass

        elif token:
            st.session_state.email = email if email > "" else "No name"
            st.session_state.token = token
            st.success(f"{label} successful!")

        else:
            st.error(f"{label} failed. Please try again.")

        st.html("</span>")





if ST_TOKEN in st.session_state:

    placeholder.empty()  # Clear the placeholder
    
    st.success(f"{st.session_state.email}, you are logged in!")

    token = st.session_state.token

    # prediction form
    st.markdown("## Prediction Form")

    fields = [
        { "id": "glucosa", "name": "Glucosa", "type": "int", "min": 0, "max": 500 },
        { "id": "hemoglobina", "name": "Hemoglobina", "type": "options", "options": ["Si", "No"] }
    ]

    payload, with_error = get_payload(fields)

    col1, col2 = st.columns([1, 5])
    response = False
    with col1:

        # Predict button
        if st.button("Predict"):
            
            #st.markdown(f"with_error {with_error}")
            st.session_state[ST_PREDICT] = True

            if with_error:
                pass

            else:
                response = m_predict(token, payload)

        else: with_error = False

    with col2:
        if st.button("Re-start", key=ST_RESTART):
            pass

    if response:

        st.write(f"**Payload:** {payload}")

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


    # Footer
    st.markdown("<hr style='border:2px solid #4B89DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #4B89DC;'>2025 Hospitalization predict App</p>",
        unsafe_allow_html=True,
    )
