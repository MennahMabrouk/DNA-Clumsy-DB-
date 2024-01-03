import streamlit as st
from Project.theme_utils import set_theme
import re
import cx_Oracle
from Project.gallary import display_gallery
from Project.db_utils import get_oracle_connection_string
import time  # Import the time module for a delay

def sign_up(connection_string, username, password, user_type, phone_number, email, gender):
    try:
        # Establish the connection (you might want to use the existing connection)
        connection = cx_Oracle.connect(connection_string)

        # Create a cursor
        cursor = connection.cursor()

        # Get the next value from the sequence for User_ID
        cursor.execute("SELECT user_id_sequence.NEXTVAL FROM dual")
        user_id = cursor.fetchone()[0]

        # Print or display the data for debugging
        st.write(f"Inserting data into Users table: {user_id} {username}, {password}, {user_type}, {phone_number}, {email}, {gender}")

        # Insert user data into the 'Users' table
        cursor.execute("""
            INSERT INTO Users (User_ID, User_name, Pass, User_type, Phone_No, Email, Gender)
            VALUES (:user_id, :username, :password, :user_type, :phone_number, :email, :gender)
        """, {
            'user_id': user_id,
            'username': username,
            'password': password,
            'user_type': user_type,
            'phone_number': phone_number,
            'email': email,
            'gender': gender
        })

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        st.success("Sign up successful!")
        # Delay for 3 seconds before calling the sign_up_success function
        time.sleep(3)
        sign_up_success()

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        st.error(f"DatabaseError: {error}")
        # Handle the error appropriately

def sign_up_success():
    # Code for actions to be taken after successful sign-up
    st.write("Sign up success action here")
    display_gallery()

def show():
    # Set theme to "dark_purple"
    set_theme("dark_purple")

    st.title("Select an Option")

    # User choice: Sign Up or Sign In
    choice = st.radio("", ["Sign Up", "Sign In"])

    if choice == "Sign Up":
        st.subheader("Sign Up")

        # Necessary details for Sign Up
        username = st.text_input("Username for signup")
        password = st.text_input("Password for signup", type="password")
        password_repeat = st.text_input("Repeat Password for signup", type="password")
        user_type = st.selectbox("User type:", ["Student", "Researcher", "Academic", "Admin"])
        phone_number = st.text_input("Phone number:")
        email = st.text_input("Email:")
        gender = st.radio("Gender:", ["Male", "Female"])

        # Password confirmation and validation for Sign Up
        if password != password_repeat:
            st.warning("Passwords do not match. Please re-enter.")
        elif len(password) < 8 or not any(char.isupper() for char in password) or not re.search("[@#$%^&+=]", password):
            st.warning("Password Requirements: \n"
                       "\n • At least 8 characters long"
                       "\n • At least one uppercase letter"
                       "\n • At least one symbol (@#$%^&+=)")
        else:
            st.success("Password is valid.")

        # Get the connection string
        connection_string = get_oracle_connection_string()

        # Display Sign Up button
        if st.button("Sign Up"):
            # Additional actions for Sign Up
            sign_up(connection_string, username, password, user_type, phone_number, email, gender)

    elif choice == "Sign In":
        st.subheader("Sign In")

        # Necessary details for Sign In
        identifier = st.text_input("Username or Email for sign-in")
        password = st.text_input("Password for sign-in", type="password")

        # Display Sign In button
        if st.button("Sign In"):
            # Additional actions for Sign In
            connection_string = get_oracle_connection_string()
            sign_in(connection_string, identifier, password)

# Set default theme to "dark_purple"
set_theme("dark_purple")

# Call the show function directly
show()

def sign_in(connection_string, identifier, password):
    try:
        # Establish the connection
        connection = cx_Oracle.connect(connection_string)

        # Create a cursor
        cursor = connection.cursor()

        # Check if the identifier is an email or username
        if '@' in identifier:
            query = "SELECT * FROM Users WHERE Email = :identifier AND Pass = :password"
        else:
            query = "SELECT * FROM Users WHERE User_name = :identifier AND Pass = :password"

        # Execute the query
        cursor.execute(query, {'identifier': identifier, 'password': password})

        # Fetch the user data
        user_data = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        if user_data:
            st.success("Sign in successful!")
            # Code for actions to be taken after successful sign-in
            # You can customize this based on your requirements
            st.write(f"Welcome, {user_data[1]}!")
            display_gallery()

        else:
            st.warning("Invalid username/email or password. Please try again.")

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        st.error(f"DatabaseError: {error}")
        # Handle the error appropriately

