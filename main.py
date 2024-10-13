import streamlit as st
import requests
import os
#from dotenv import load_dotenv

#load_dotenv()

# API URL
API_URL = os.environ.get("API_URL_TEST")

def register_user(username, password, security_code):
    """Registers the user with the FastAPI backend."""
    payload = {
        "username": username,
        "password": password,
        "security_code": security_code
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
        return response.json(), None
    except requests.exceptions.HTTPError as errh:
        if response.status_code == 400:
            return None, "Username already exists or invalid security code."
        return None, "HTTP Error: {}".format(errh)
    except requests.exceptions.ConnectionError as errc:
        return None, "Error Connecting: {}".format(errc)
    except requests.exceptions.Timeout as errt:
        return None, "Timeout Error: {}".format(errt)
    except requests.exceptions.RequestException as err:
        return None, "Unexpected Error: {}".format(err)

# Streamlit UI
st.title("Register User")

# Input fields
username = st.text_input("Username", placeholder="Enter your username")
password = st.text_input("Password", type="password", placeholder="Enter your password")
security_code = st.text_input("Security Code", placeholder="Enter your security code")

if st.button("Register"):
    if username and password and security_code:
        user, error = register_user(username, password, security_code)
        if user:
            st.success("User registered successfully!")
        else:
            st.error(f"Registration failed: {error}")
    else:
        st.warning("Please fill in all fields.")
