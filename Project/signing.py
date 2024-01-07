import streamlit as st
import re
import cx_Oracle
from Project.theme_utils import set_theme
from Project.gallary import display_gallery
from Project.db_utils import get_oracle_connection_string
import time

class SessionState:
    def __init__(self):
        self.sign_up_key = "choice_sign_up"

def sign_up(connection_string, username, password, user_type, phone_number, email, gender, password_repeat):
    try:
        # Establish the connection (you might want to use the existing connection)
        connection = cx_Oracle.connect(connection_string)

        # Create a cursor
        cursor = connection.cursor()

        # Validate phone number
        phone_number_valid = re.match(r'^01\d{9}$', phone_number)

        if not phone_number_valid:
            st.warning("Invalid phone number. Please enter an Egyptian number without spaces or special characters.")
            return  

        # Validate password
        password_valid = (
            len(password) >= 8
            and any(char.isupper() for char in password)
            and any(char in r"@#$%^&+=" for char in password)
            and all(char.isascii() for char in password)
        )

        if not password_valid:
            st.warning("Password Requirements: \n"
                       "\n • At least 8 characters long"
                       "\n • At least one uppercase letter"
                       "\n • At least one symbol (@#$%^&+=)"
                       "\n • Must be in English (ASCII characters)")
            return  
        
        # Validate email
        email_valid = re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

        if not email_valid:
            st.warning("Invalid email address. Please enter a valid email.")
            return 

        # Check if the username already exists
        cursor.execute("SELECT COUNT(*) FROM Users WHERE User_name = :username", {'username': username})
        username_exists = cursor.fetchone()[0]

        if username_exists > 0:
            st.warning("Username already exists. Please choose a different username.")
            return  # Exit the function if the username already exists

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

def sign_up_success():
    # Code for actions to be taken after successful sign-up
    st.write("Sign up success action here")
    display_gallery()

def show():
    # Set theme to "dark_purple"
    set_theme("dark_purple")

    st.title("Select an Option")

    # Get the session state
    session_state = SessionState()

    # User choice: Sign Up, Sign In, or Delete Account
    choice = st.radio("", ["Sign Up", "Sign In", "Delete Account"], key=session_state.sign_up_key)

    if choice == "Sign Up":
        st.subheader("Sign Up")

        # Necessary details for Sign Up
        username = st.text_input("Username for signup")
        password = st.text_input("Password for signup", type="password")
        password_repeat = st.text_input("Repeat Password for signup", type="password")

        # Validate password
        password_valid = (
            len(password) >= 8
            and any(char.isupper() for char in password)
            and any(char in r"@#$%^&+=" for char in password)
            and all(char.isascii() for char in password)
        )

        if not password_valid:
            st.warning("Password Requirements: \n"
                       "\n • At least 8 characters long"
                       "\n • At least one uppercase letter"
                       "\n • At least one symbol (@#$%^&+=)"
                       "\n • Must be in English (ASCII characters)")
            return  # Exit the function if the password is not valid

        # Other user details
        user_type = st.selectbox("User type:", ["Student", "Researcher", "Academic", "Admin"])
        phone_number = st.text_input("Phone number:")

        # Validate phone number
        phone_number_valid = re.match(r'^01\d{9}$', phone_number)

        if not phone_number_valid:
            st.warning("Invalid phone number. Please enter a 10-digit number without spaces or special characters.")
            return  # Exit the function if the phone number is not valid

        email = st.text_input("Email:")
        gender = st.radio("Gender:", ["Male", "Female"])

        # Get the connection string
        connection_string = get_oracle_connection_string()

        # Display Sign Up button
        if st.button("Sign Up") and password_valid and phone_number_valid:
            # Additional actions for Sign Up
            sign_up(connection_string, username, password, user_type, phone_number, email, gender, password_repeat)

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

    elif choice == "Delete Account":
        st.subheader("Delete Account")

        # Necessary details for account deletion
        username = st.text_input("Username for account deletion")
        password = st.text_input("Password for account deletion", type="password")

        # Display Delete Account button
        if st.button("Delete Account"):
            # Additional actions for account deletion
            connection_string = get_oracle_connection_string()
            delete_account(connection_string, username, password)

            # Display alert based on the session variable
            if st.session_state.account_deleted:
                st.success("Account deleted successfully!")
            else:
                st.warning("Invalid username or password. Please try again.")

            # Clear the session variable
            st.session_state.account_deleted = None

if __name__ == "__main__":
    show()


def delete_account(connection_string, username, password):
    try:
        # Establish the connection
        connection = cx_Oracle.connect(connection_string)

        # Create a cursor
        cursor = connection.cursor()

        # Check if the provided username and password match the user's credentials
        query = "SELECT * FROM Users WHERE User_name = :username AND Pass = :password"
        cursor.execute(query, {'username': username, 'password': password})
        user_data = cursor.fetchone()

        if user_data:
            # Delete the user account
            delete_query = "DELETE FROM Users WHERE User_ID = :user_id"
            cursor.execute(delete_query, {'user_id': user_data[0]})
            connection.commit()

            # Set session variable for successful deletion
            st.session_state.account_deleted = True
        else:
            # Set session variable for unsuccessful deletion
            st.session_state.account_deleted = False

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        st.error(f"DatabaseError: {error}")
    finally:
        cursor.close()
        connection.close()


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
    finally:
        cursor.close()
        connection.close()
