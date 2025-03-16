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

ST_LOGIN = "Login"
ST_REGISTER = "Register"
ST_TOKEN = "token"
ST_RESTART = "restart"
ST_ERROR = "error"
ST_INITIALS = "initials"
ST_DATA = "data"

TYPE_INT = "int"
TYPE_FLOAT = "float"
TYPE_OPTIONS = "options"

VERSION = "2.0"
TEST = False


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

def get_payload():
    
    """
    fields = []
    for i in range(50):
         fields.append({ "id": str(i), "name": f"Field {i}", "type": TYPE_INT, "min": 0, "max": 500, 
                            "value" : st.session_state[ST_INITIALS][i] })
    """
    
    fields = [

        { "id": "r4dadage", "name": "Age of the respondent's father", "type": TYPE_FLOAT } , 
        { "id": "r4agey", "name": "Age of the respondent in years", "type": TYPE_FLOAT } , 
        { "id": "r4momage", "name": "Age of the respondent's mother", "type": TYPE_FLOAT } , 
        { "id": "r4wthh", "name": "Household weight", "type": TYPE_FLOAT } , 
        { "id": "r4wtresp", "name": "Respondent weight", "type": TYPE_FLOAT } , 
        { "id": "rafeduc_m", "name": "Father's education level", "type": TYPE_FLOAT } , 
        { "id": "rameduc_m", "name": "Mother's education level", "type": TYPE_FLOAT } , 
        { "id": "r4shlt", "name": "Self-reported health", "type": TYPE_FLOAT } , 
        { "id": "r4sight", "name": "Vision problems", "type": TYPE_FLOAT } , 
        { "id": "r4hearing", "name": "Hearing problems", "type": TYPE_FLOAT } , 
        { "id": "r4hltc", "name": "Change in health compared to two years ago", "type": TYPE_FLOAT } , 
        { "id": "r4painlv", "name": "Level of pain", "type": TYPE_FLOAT } , 
        { "id": "r4cholst", "name": "Cholesterol level", "type": TYPE_FLOAT } , 
        { "id": "r4arthre", "name": "Diagnosis of arthritis", "type": TYPE_FLOAT } , 
        { "id": "r4respe", "name": "Diagnosis of respiratory diseases", "type": TYPE_FLOAT } , 
        { "id": "r4vigact", "name": "Vigorous physical activity", "type": TYPE_FLOAT } , 
        { "id": "r4wakeup", "name": "Difficulty waking up", "type": TYPE_FLOAT } , 
        { "id": "r4joga", "name": "Practice of yoga", "type": TYPE_FLOAT } , 
        { "id": "r4rxdiabi", "name": "Use of diabetes medication", "type": TYPE_FLOAT } , 
        { "id": "r4rested", "name": "Feeling rested", "type": TYPE_FLOAT } , 
        { "id": "r4wakent", "name": "Time taken to wake up", "type": TYPE_FLOAT } , 
        { "id": "r4rxdiabo", "name": "Use of diabetes medication", "type": TYPE_FLOAT } , 
        { "id": "r4stoopa", "name": "Difficulty stooping", "type": TYPE_FLOAT } , 
        { "id": "r4sleepr", "name": "Sleep quality", "type": TYPE_FLOAT } , 
        { "id": "r4doctim1y", "name": "Number of doctor visits in the last year", "type": TYPE_FLOAT } , 
        { "id": "r4hosp1y", "name": "Number of hospitalizations in the last year", "type": TYPE_FLOAT } , 
        { "id": "r4hspnit1y", "name": "Number of nights in the hospital in the last year", "type": TYPE_FLOAT } , 
        { "id": "r4oopmd1y", "name": "Out-of-pocket medical expenses in the last year", "type": TYPE_FLOAT } , 
        { "id": "r4dentim1y", "name": "Number of dentist visits in the last year", "type": TYPE_FLOAT } , 
        { "id": "r4imrc8", "name": "Immediate recall score (8 items)", "type": TYPE_FLOAT } , 
        { "id": "r4slfmem", "name": "Self-reported memory", "type": TYPE_FLOAT } , 
        { "id": "r4verbf", "name": "Verbal fluency score", "type": TYPE_FLOAT } , 
        { "id": "r4ser7", "name": "Score on the serial 7s test", "type": TYPE_FLOAT } , 
        { "id": "r4tr16", "name": "Delayed recall score (16 items)", "type": TYPE_FLOAT } , 
        { "id": "r4ipent", "name": "Total income from public pensions", "type": TYPE_FLOAT } , 
        { "id": "r4tpamt", "name": "Total amount of private transfers received", "type": TYPE_FLOAT } , 
        { "id": "r4iearn", "name": "Labor income", "type": TYPE_FLOAT } , 
        { "id": "r4livsib", "name": "Number of living siblings", "type": TYPE_FLOAT } , 
        { "id": "raevbrn", "name": "Number of children ever born", "type": TYPE_FLOAT } , 
        { "id": "r4rfcntx_m", "name": "Frequency of contact with friends and relatives", "type": TYPE_FLOAT } , 
        { "id": "r4decsib", "name": "Number of deceased siblings", "type": TYPE_FLOAT } , 
        { "id": "r4igxfr", "name": "Intergenerational transfers", "type": TYPE_FLOAT } , 
        { "id": "r4height", "name": "Height of the respondent", "type": TYPE_FLOAT } , 
        { "id": "r4weight", "name": "Weight of the respondent", "type": TYPE_FLOAT } , 
        { "id": "r4bmi", "name": "Body Mass Index (BMI)", "type": TYPE_FLOAT } , 
        { "id": "r4vscan", "name": "Use of vascular scan", "type": TYPE_FLOAT } , 
        { "id": "r4gcaresckd_m", "name": "Frequency of caring for a sick or disabled adult", "type": TYPE_FLOAT } , 
        { "id": "r4lsatsc3", "name": "Life satisfaction", "type": TYPE_FLOAT } , 
        { "id": "r4socact_m", "name": "Social activities", "type": TYPE_FLOAT } , 
        { "id": "r4enlife", "name": "Satisfaction with life", "type": TYPE_FLOAT } , 
    ]
    
    df = st.session_state[ST_DATA]

    cats = [f["id"] for f in fields
                if df[f["id"]].dtype.name == 'category']
                
    for id in cats:
        field = next((item for item in fields if item['id'] == id), None)
        unique_names = np.sort(df[id].dropna().unique()).tolist()
        #df[id].dropna().unique().tolist()

        field["type"] = TYPE_OPTIONS
        field["options"] = unique_names
        #field["value"] = unique_names[0]


    payload = {}
    with_error = False

    #print("State In", st.session_state)

    for field in fields:

        field_error = False

        #st.write(f"**{field}**")
        
        if field["type"] == TYPE_OPTIONS:
            initial = field["value"] if "value" in field else ""
            default_index = field["options"].index(initial) if initial in field["options"] else 0
            value = st.selectbox(field["name"], field["options"], index=default_index, key=field["id"])

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

#print("State token?", st.session_state[ST_TOKEN] if ST_TOKEN in st.session_state else "No token")

if not ST_DATA in st.session_state:

    st.write("Loading data...")
    DATA = os.path.join(os.path.dirname(__file__), 'H_MHAS_c2.dta')

    # Find categorical fields
    st.session_state[ST_DATA] = pd.read_stata(DATA)


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

                    if TEST:
                        st.session_state.token = "Test"

                    elif token is None:
                        st.error("Login failed. Please check your credentials.")

                    else:
                        st.session_state.token = token
                        st.success("Login successful!")

            with col2:

                if st.button(ST_REGISTER):
                    st.session_state[ST_REGISTER] = True
                    st.rerun()  # Reinicia la app

#---------------------------------------------------------------------------------------------------------------
#if not check_state(ST_INITIALS):
#    st.session_state[ST_INITIALS] = [random.randint(0, 500) for _ in range(50)]

if ST_TOKEN in st.session_state:

    placeholder.empty()  # Clear the placeholder

    st.success(f"You are logged in!")

    token = st.session_state.token


    # prediction form
    st.markdown("## Prediction Form")

    payload = get_payload()


    col1, col2 = st.columns([1, 5])
    response = False
    with col1:

        # Predict button
        if st.button("Predict"):
            response = predict(token, payload)

    with col2:
        if st.button("Re-start", key=ST_RESTART):
            pass


    #st.write("Payload", payload)

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
