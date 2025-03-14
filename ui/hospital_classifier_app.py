from typing import Optional
import json
import requests
import streamlit as st
from app.settings import API_BASE_URL
from PIL import Image
import random

ST_LOGIN = "Login"
ST_REGISTER = "Register"
ST_TOKEN = "token"
ST_RESTART = "restart"
ST_ERROR = "error"
ST_INITIALS = "initials"

TYPE_INT = "int"
TYPE_FLOAT = "float"
TYPE_OPTIONS = "options"

VERSION = "1.2"

def register(username: str, password: str, name: str) -> Optional[str]:
    """This function calls the register endpoint of the API to create a new user.

    Args:
        username (str): email of the user
        password (str): password of the user
        name (str): name of the user

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
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    #  3. Make a POST request to the predict endpoint.
    # TODO: Check the predict API (MD) 
    url = f"{API_BASE_URL}/model/predict"
    response = requests.post(url, headers=headers, json=form_data)

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

    #print("State In", st.session_state)

    for field in fields:

        field_error = False

        if field["type"] == TYPE_OPTIONS:
            initial = field["value"] if "value" in field else ""
            value = st.selectbox(field["name"], field["options"], value=initial)

        else:
        
            initial = field["value"] if "value" in field else 0

            min = field["min"] if "min" in field else None
            max = field["max"] if "max" in field else None

            if min != None and max != None:
                message = f"between {min} and {max}"
            
            elif min != None:
                message = f"greater than {min}"

            elif max != None:
                message = f"less than {max}"

            else:
                message = ""

            message = f"Enter a number {message}"

            value = st.text_input(field["name"], placeholder=message, value=initial)

            if value:

                try:
                    number = float(value)  # Convert input to a number
                    
                    if field["type"] == "int" and not number.is_integer():
                        message = "Enter a whole number"
                        field_error = True

                    elif min == None and max == None:
                        pass

                    elif min == None and not number <= max \
                        or max == None and not number >= min \
                        or not (min <= number <= max):
                        field_error = True

                except ValueError:
                    message = "Enter a valid number"
                    field_error = True

            elif not ST_ERROR in st.session_state:
                pass

            else:
                message = "Enter a valid number"
                field_error = True

        payload[field["id"]] = value

        if field_error:
            st.error(f"{field['name']}: {message}!")
            with_error = True


    st.session_state[ST_ERROR] = with_error
    return payload



# Interfaz de usuario
#st.set_page_config(page_title="Hospitalization Risks", page_icon="📷✈️")
st.set_page_config(page_title="Hospitalization Risks", page_icon="🏥")


st.markdown(
    f"<h1 style='text-align: center; color: #4B89DC;'>Hospitalization Risks</h1>",
    unsafe_allow_html=True,
)

st.write("Version ", VERSION)

if check_state(ST_RESTART):
    check_state(ST_TOKEN, True)
    check_state(ST_ERROR, True)
    check_state(ST_INITIALS, True)



# Create a placeholder
placeholder = st.empty()
with placeholder.container():

    # Formulario de login
    if not check_state(ST_TOKEN):

        if check_state(ST_REGISTER):

            st.markdown(f"## {ST_REGISTER}")

            name = st.text_input("Name")
            username = st.text_input("E-Mail")
            password = st.text_input("Password", type="password")

            if st.button("Confirm"):
                token = register(username, password, name)
                if token:
                    st.session_state.token = token
                    st.success("Register successful!")
                else:
                    st.error("Register failed. Please check your credentials.")

        else:

            st.markdown("## Login")
            username = st.text_input("E-Mail", value="admin@example.com")
            password = st.text_input("Password", type="password", value="admin")

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
                if st.button(ST_REGISTER):
                    st.session_state[ST_REGISTER] = True
                    st.rerun()  # Reinicia la app

#---------------------------------------------------------------------------------------------------------------
if not check_state(ST_INITIALS):
    st.session_state[ST_INITIALS] = [random.randint(0, 500) for _ in range(50)]

if ST_TOKEN in st.session_state:

    placeholder.empty()  # Clear the placeholder

    st.success(f"You are logged in!")

    token = st.session_state.token


    # prediction form
    st.markdown("## Prediction Form")

    # d = { "0" : 12937 , "1" : 12938 .... "49" : 18877 }

    
    # fields = [
    #    { "id": "hemoglobina", "name": "Hemoglobina", "type": TYPE_OPTIONS, "options": ["Si", "No"] },
    #    { "id": "hematies", "name": "Hematies", "type": TYPE_INT },
    #    { "id": "glucosa", "name": "Glucosa", "type": TYPE_INT, "min": 0, "max": 500 },
    #]


    fields = []
    for i in range(50):
         fields.append({ "id": str(i), "name": f"Field {i}", "type": TYPE_INT, "min": 0, "max": 500, 
                            "value" : st.session_state[ST_INITIALS][i] })

    payload = get_payload(fields)


    col1, col2 = st.columns([1, 5])
    response = False
    with col1:

        # Predict button
        if st.button("Predict"):
            response = predict(token, payload)

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


    elif check_state(ST_ERROR):
        st.error("Please correct the errors before predicting.")


    # Footer
    st.markdown("<hr style='border:2px solid #4B89DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #4B89DC;'>2025 Hospitalization predict App</p>",
        unsafe_allow_html=True,
    )
