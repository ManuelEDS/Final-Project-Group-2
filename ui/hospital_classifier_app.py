from typing import Optional
import json
import requests
import streamlit as st
from app.settings import API_BASE_URL
from PIL import Image
import random
import pandas as pd
import os
import numpy as np

TYPE_INT = "int"
TYPE_FLOAT = "float"
TYPE_OPTIONS = "options"
TYPE_BINARY = "binary"

VERSION = "2.0.1"


def register(username: str, password: str, name: str) -> Optional[str]:
    """This function calls the register endpoint of the API to create a new user.

    Args:
        username (str): email of the user
        password (str): password of the user
        name (str): name of the user

    Returns:
        Optional[str]: token if registration is successful, None otherwise
    """

    # Check if any of the fields are empty
    if username == "" or password == "" or name == "":
        st.error("Please fill in all fields.")
        return

    # Steps to Build the `register` Function:
    #  1. Construct the API endpoint URL using `API_BASE_URL` and `/register`.
    url = f"{API_BASE_URL}/user"

    #  2. Set up the request headers with `accept: application/json` and
    #     `Content-Type: application/x-www-form-urlencoded`.
    headers = { 
        "accept" : "application/json",
        #"Content-Type" : "application/x-www-form-urlencoded" 
    }

    #  3. Prepare the data payload with fields: `grant_type`, `username`, `password`,
    #     `scope`, `client_id`, and `client_secret`.
    payload = { 
        "email": username,
        "password": password,
        "name": name,
    }

    #  4. Use `requests.post()` to send the API request with the URL, headers,
    #     and data payload.
    token = None

    try:
        # TODO: Check the register API (MD) 
        response = requests.post(url, headers=headers, json=payload)

        #  5. Check if the response status code is `201`.
        #  6. If successful, go login and extract the token from the JSON response.
        if response.status_code == 201:
            token = login(username, password)

        else:

            try:
                # Check if "detail" is a list and extract the first message
                detail = response.json().get("detail", "An error occurred.")
                if isinstance(detail, list) and len(detail) > 0:
                    error_message = detail[0].get("msg", "An error occurred.")
                else:
                    error_message = detail  # Use the detail directly if it's not a list

            # If the response is not JSON, catch the exception and use the response text
            except json.JSONDecodeError:
                error_message = "An error occurred, and the response could not be parsed."

            # Display the error message
            st.error(f"Registration failed, {error_message}")

    # Connection error
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check..")

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

    if username == "" or password == "":
        st.error("Please fill in all fields.")
        return

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

    token = None

    try:
        # TODO: Check the login API (MD) 
        response = requests.post(url, headers=headers, data=payload)

        #  5. Check if the response status code is `200`.
        #  6. If successful, extract the token from the JSON response.
        #  7. Return the token if login is successful, otherwise return `None`.
        #  8. Test the function with various inputs.
        if response.status_code == 200:
            token = response.json()["access_token"]
        else:
            st.error("Login failed. Please check your credentials.")

    # Connection error
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check..")


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

    try:
        # Predict the hospitalization risk
        response = requests.post(url, headers=headers, json=form_data)

    # Connection error
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check..")
        return None

    #  4. Return the response.
    return response

def check_state(state: str, remove: bool = False):

    # Check if the state exists or delete
    if state in st.session_state:
        value = st.session_state[state]
        if remove: del st.session_state[state]
        
        return value 

    return False

def get_payload():

    # Prepare the fields for the form
    fields = [
        { "id": "r4agey", "name": "Age of the respondent in years", "type": TYPE_INT, "values": (50, 120), "section": "A - Demographics, Identifiers, and Weights" },
        { "id": "r4rxdiab", "name": "Use of diabetes medication", "type": TYPE_BINARY, "section": "B - Health" },
        { "id": "r4mobila", "name": "Mobility limitations (0-No limitations... 5-Total limitations)", "type": TYPE_INT, "values": (0, 5), "section": "B - Health"},
        { "id": "r4nagi10", "name": "NAGI functional limitations (0-No limitations... 10-Total limitations)", "type": TYPE_INT, "values": (0, 10), "section": "B - Health" },
        { "id": "r4cholst", "name": "High cholesterol level", "type": TYPE_BINARY, "section": "B - Health" },
        { "id": "r4diabe", "name": "Diagnosis of diabetes", "type": TYPE_BINARY, "section": "B - Health" },
        { "id": "r4walk1", "name": "Difficulty walking one block", "type": TYPE_BINARY, "section": "B - Health" },
        { "id": "r4arthre", "name": "Diagnosis of arthritis", "type": TYPE_BINARY, "section": "B - Health" },
        { "id": "r4grossa", "name": "Gross motor skills limitations", "type": TYPE_BINARY, "section": "B - Health" },
        { "id": "r4hosp1y", "name": "Hospital stay in the last year", "type": TYPE_BINARY, "section": "C - Health Care Utilization and Insurance" },
        { "id": "r4doctim1y", "name": "Number of doctor visits in the last year", "type": TYPE_INT, "values": (0, 365), "section": "C - Health Care Utilization and Insurance" },
        { "id": "r4hspnit1y", "name": "Number of nights in the hospital in the last year", "type": TYPE_INT, "values": (0, 365), 
            "section": "C - Health Care Utilization and Insurance" }
    ]

    payload = {}
    with_error = False

    # for each field in the form, depending of the type, show the input
    for field in fields:

        field_error = False

        id = field["id"]

        # Show the section title
        if id == "r4agey" or id == "r4rxdiab" or id == "r4hosp1y":
            st.markdown(f"### {field['section']}")
        
        name = field["name"] + "?"

        # Show the binary input field
        if field["type"] == TYPE_BINARY:
            checked = st.checkbox(name, value=False, key=id)
            value = 1 if checked else 0

        # Show the options input field
        elif field["type"] == TYPE_OPTIONS:
            initial = field["value"] if "value" in field else ""
            default_index = field["options"].index(initial) if initial in field["options"] else 0
            value = st.selectbox(name, field["options"], index=default_index, key=id)

        # Show the integer / float input field
        else:
        
            initial = field["value"] if "value" in field else "0"

            # Check if the field has a range to validate
            min, max = None, None
            if "values" in field:
                min, max = field["values"]

            if min != None and max != None:
                message = f"between {min} and {max}"
            
            elif min != None:
                message = f"greater than {min}"

            elif max != None:
                message = f"less than {max}"

            else:
                message = ""

            message = f"Enter a number {message}"

            # Show the input field
            value = st.text_input(name, placeholder=message, value=initial, key=id)

            # Validate the numeric input field
            if value:

                try:
                    number = float(value)  # Convert input to a number
                    
                    if field["type"] == TYPE_INT and not number.is_integer():
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

        payload[id] = value

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

ST_TOKEN = "token"
ST_RESTART = "restart"
ST_ERROR = "error"
ST_DATA = "data"

# if restart, delete the token and the error
if check_state(ST_RESTART):
    check_state(ST_TOKEN, True)
    check_state(ST_ERROR, True)

# Create a placeholder
placeholder = st.empty()
with placeholder.container():

    # Create two columns for the login and register forms
    col1, col2 = st.columns(2)

    with col1:

        # Login Form
        with st.form(key="login_form"):
            st.markdown("## Login")
            username = st.text_input("E-Mail") #, value="admin@example.com")
            password = st.text_input("Password", type="password") #, value="admin")

            # Add a submit button for the login form
            login_button = st.form_submit_button("Login")

            if login_button:
                token = login(username, password)

                if token:
                    st.session_state.token = token

    with col2:

        # Register Form
        with st.form(key="register_form"):
            st.markdown(f"## Register")

            name = st.text_input("Name")
            username = st.text_input("E-Mail")
            password = st.text_input("Password", type="password")

            # Add a submit button for the register form
            register_button = st.form_submit_button("Register")

            if register_button:
                token = register(username, password, name)

                if token:
                    st.session_state.token = token





# Check if the user is logged in
if ST_TOKEN in st.session_state:

    placeholder.empty()  # Clear the placeholder

    st.success(f"You are logged in!")

    token = st.session_state.token


    # prediction form
    st.markdown("## Prediction Form")

    payload = get_payload()

    response = False

    # Predict button
    if st.button("Predict", disabled=check_state(ST_ERROR)):
        response = predict(token, payload)

    if st.button("Re-Start", key=ST_RESTART):
        pass

    if response:

        # Check if the response is successful, show the prediction
        if response.status_code == 200:
            result = response.json()

            #data = f"Prediction: {result['prediction']} <br> Score: {format(result['score'], '.2f')}"  
            #background = "#c8fb8a" if float(result['prediction'])<1 else "#fbde8a"

            score = f"{format(result['score']*100, '.0f')}%"

            if float(result['prediction'])<1:
                st.success(f"Probability: {score}, low chances of being hospitalized")

            else:
                st.error(f"Probability: {score}, high chances of being hospitalized!")

            #st.write(f"Prediction: {result['prediction']}") 
            #st.write(f"Score: {format(result['score'], '.2f')}") 
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
