import streamlit as st
import requests
import os
import re

# API URL
API_URL = os.environ.get("API_URL")

REGISTRATION_INFO = """
### Registration Instructions

**1. Username Creation:**

Please create your username using the following format (use lowercase letters and follow the sequence exactly without spaces):

- **Step 1**: First letter of your mother’s first name (or the most important female reference person in your childhood).
- **Step 2**: First letter of your father’s first name (or the most important male reference person in your childhood).
- **Step 3**: First letter of the city where you were born.
- **Step 4**: Birth month of your mother (or the most important female reference person in your childhood) as a two-digit number (01-12).
- **Step 5**: Birth year of your father (or the most important male reference person in your childhood) in four digits (yyyy).

**Example**: If your mother's name is Helen, your father's name is Andrew, you were born in Geneva, your mother’s birth month is June (06), and your father’s birth year is 1960, your username would be:

`hag061960`

**2. Registration Process:**

- **Step 1**: Enter the username you generated using the above instructions.
- **Step 2**: Create a strong password for your account.
- **Step 3**: Enter the unique security code provided to you.

Once you've filled in all the required information, click **Register** to complete the process.

If any issues arise, please check that all information is entered correctly or contact support for assistance.
"""

# Function to validate the username format
def validate_username(username):
    pattern = r"^[a-z]{3}\d{2}\d{4}$"  # 3 lowercase letters, 2 digits for month, 4 digits for year
    return re.match(pattern, username)

# Function to register the user
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
st.title("OM Register User")
st.markdown(REGISTRATION_INFO)

# Input fields
username = st.text_input("Username", placeholder="Enter your username")
password = st.text_input("Password", type="password", placeholder="Enter your password")
password_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
security_code = st.text_input("Security Code", placeholder="Enter your security code")

if st.button("Register"):
    # Username validation
    if not validate_username(username):
        st.error("Invalid username format. Please follow the instructions.")
    # Password validation
    elif password != password_confirm:
        st.error("Passwords do not match. Please try again.")
    elif not password or not password_confirm:
        st.warning("Please fill in all password fields.")
    # All fields are valid, proceed with registration
    elif username and password and password_confirm and security_code:
        user, error = register_user(username, password, security_code)
        if user:
            st.success("User registered successfully!")
        else:
            st.error(f"Registration failed: {error}")
    else:
        st.warning("Please fill in all fields.")

