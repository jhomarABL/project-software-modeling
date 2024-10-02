
import mysql.connector
import hashlib

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to the database
def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="",  
        database="app_db"
    )


def register_user(username, password):
    db = connect()
    cursor = db.cursor()
    try:
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        cursor.execute(query, (username, hash_password(password)))
        db.commit()
        print(f"User '{username}' registered successfully.")
    except mysql.connector.IntegrityError:
        print("Username already exists.")
    finally:
        cursor.close()
        db.close()


def login_user(username, password):
    db = connect()
    cursor = db.cursor()
    try:
        query = "SELECT password_hash FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result and result[0] == hash_password(password):
            print(f"Login successful. Welcome, {username}!")
            return True
        else:
            print("Invalid credentials.")
            return False
    finally:
        cursor.close()
        db.close()


def process_command(command, username, password):
    if command == "register":
        register_user(username, password)
    elif command == "login":
        login_user(username, password)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python user_management.py [command] [username] [password]")
    else:
        command = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        process_command(command, username, password)
