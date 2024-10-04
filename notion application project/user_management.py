"""
Authors: Jhomar Armando Bojaca Landinez <jabojacal@udistrital.edu.co>
         Santiago Alejandro Guada Bohorquez <saguadab@udistrital.edu.co>

This file is part of notion application project.

notion application project is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

notion application project is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with notion application project. If not, see <https://www.gnu.org/licenses/>.
"""
import mysql.connector
import hashlib

def hash_password(password):
    """
    Hashes a password using SHA-256.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The hexadecimal SHA-256 hash of the password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def connect():
    """
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: A connection object to the MySQL database.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="",  
        database="app_db"
    )

def register_user(username, password):
    """
    Registers a new user by inserting their username and hashed password into the database.

    Args:
        username (str): The desired username for the new user.
        password (str): The plain-text password for the new user.

    Effects:
        Inserts a new record into the 'users' table with the provided username and hashed password.
        Prints a success message or an error message if the username already exists.
    """
    db = connect()
    cursor = db.cursor()
    try:
        # SQL query to insert a new user
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        # Execute the query with the provided username and hashed password
        cursor.execute(query, (username, hash_password(password)))
        # Commit the transaction to the database
        db.commit()
        print(f"User '{username}' registered successfully.")
    except mysql.connector.IntegrityError:
        # Handle the error if the username already exists (unique constraint violation)
        print("Username already exists.")
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()

def login_user(username, password):
    """
    Authenticates a user by verifying their username and password.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The plain-text password provided by the user.

    Returns:
        bool: True if authentication is successful, False otherwise.

    Effects:
        Prints a success message if authentication is successful.
        Prints an error message if authentication fails.
    """
    db = connect()
    cursor = db.cursor()
    try:
        # SQL query to retrieve the hashed password for the given username
        query = "SELECT password_hash FROM users WHERE username = %s"
        # Execute the query with the provided username
        cursor.execute(query, (username,))
        # Fetch the first result from the query
        result = cursor.fetchone()

        # Check if a result was found and if the hashed passwords match
        if result and result[0] == hash_password(password):
            print(f"Login successful. Welcome, {username}!")
            return True
        else:
            print("Invalid credentials.")
            return False
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()

def process_command(command, username, password):
    """
    Processes the user command to either register or log in a user.

    Args:
        command (str): The command to execute ('register' or 'login').
        username (str): The username of the user.
        password (str): The plain-text password of the user.
    """
    if command == "register":
        register_user(username, password)
    elif command == "login":
        login_user(username, password)
    else:
        print("Unrecognized command. Use 'register' or 'login'.")

if __name__ == "__main__":
    import sys
    # Ensure that the correct number of arguments are provided
    if len(sys.argv) < 4:
        print("Usage: python user_management.py [command] [username] [password]")
    else:
        # Assign command-line arguments to variables
        command = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        # Process the command with the provided arguments
        process_command(command, username, password)
