import mysql.connector
from mysql.connector import pooling
from configparser import ConfigParser
import bcrypt
from cryptography.fernet import Fernet
import logging
from io import BytesIO
from PIL import Image
import Simon
import requests


# LOGS
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_db_config(filename='config.ini', section='database'):
    parser = ConfigParser()
    parser.read(filename)
    db_config = {}

    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file')

    return db_config

def read_encryption_key(filename='config.ini', section='encryption'):
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        return parser.get(section, 'encryption_key')
    else:
        raise Exception(f'{section} not found in the {filename} file')

db_config = read_db_config()
encryption_key = read_encryption_key()

fernet = Fernet(encryption_key)

def encrypt_cookie(cookie):
    return fernet.encrypt(cookie.encode('utf-8')).decode('utf-8')

def decrypt_cookie(encrypted_cookie):
    return fernet.decrypt(encrypted_cookie.encode('utf-8')).decode('utf-8')

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(hashed_password, password):
    # Verify if the entered password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def databaseCheckUser(username, password):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, cookie FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is not None:
            db_username, db_password, cookie = result
            if verify_password(db_password, password):
                cookie = decrypt_cookie(cookie)
                return 200, cookie
            else:
                return 403  # Unauthorized
        else:
            return 404
    except mysql.connector.Error as e:
        logger.error(f"Error checking user in the database: {e}")
        return 404
    finally:
        cursor.close()
        conn.close()

def databaseAddUser(username, password, cookie):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        encrypted_cookie = encrypt_cookie(cookie)
        cursor.execute("INSERT INTO users (username, password, cookie, studentImage) VALUES (%s, %s, %s, %s)", (username, hashed_password, encrypted_cookie, ''))
        conn.commit()
        logger.info(f"User '{username}' added to the database.")
        cursor.execute("UPDATE statistics SET users = users + 1")
        conn.commit()
    except mysql.connector.Error as e:
        logger.error(f"Error adding user to the database: {e}")
    finally:
        cursor.close()
        conn.close()

# Checks database to see if image exists.
def databaseCheckImage(username):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT studentImage FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is not None:
            image_data = result[0]
            if image_data:
                try:
                    # Attempt to open the image
                    image = Image.open(BytesIO(image_data))
                    return image_data
                except Exception as e:
                    # Handle any exception and log it
                    logger.error(f"Error opening image: {e}")
                    return None  # Invalid or unrecognized image data
            else:
                return None  # Empty image data
        else:
            return None  # Image not found in the database
    except mysql.connector.Error as e:
        logger.error(f"Error checking image in the database: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


# Downloads image from URL and adds it to database
def databaseAddImage(username, cookie):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()

        # Check if an image already exists in the database
        cursor.execute("SELECT studentImage FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        # Get the image URL using Simon.getUserProfileImageURL
        cookies = {'adAuthCookie': cookie}
        image_url = Simon.getSimonStudentImageURL(cookie)

        if image_url:
            # Download the image from the URL
            cookies = {'adAuthCookie': cookie}
            image_data = requests.get(image_url, cookies=cookies).content

            # Store the downloaded image in the database
            cursor.execute("UPDATE users SET studentImage = %s WHERE username = %s", (image_data, username))
            conn.commit()
            return image_data

    except mysql.connector.Error as e:
        logger.error(f"Error storing image in the database: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def databaseGetTheme(username):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()

        # Check if an image already exists in the database
        cursor.execute("SELECT theme FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        # Get the image URL using Simon.getUserProfileImageURL
        theme = result[0] if result else None

        return theme

    except mysql.connector.Error as e:
        logger.error(f"Error storing image in the database: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def databaseChangeTheme(username, theme):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()

        # Check if an image already exists in the database
        cursor.execute("UPDATE users SET theme = %s WHERE username = %s", (theme, username))
        conn.commit()
        print('Changed Theme')

        # Get the image URL using Simon.getUserProfileImageURL

        return 200

    except mysql.connector.Error as e:
        logger.error(f"Error storing theme in the database: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Create a connection pool
db_pool = pooling.MySQLConnectionPool(
    pool_name="main_pool",
    pool_size=5,
    **db_config
)