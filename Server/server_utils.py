import sqlite3
import json
import random

class UsersDB:

    def __init__(self):
        self.database = 'users.db'

    def connect_to_db(self):
        conn = sqlite3.connect(self.database)
        return conn

    def create_table(self):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY NOT NULL, 
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

    def insert_user(self, username, password):
        self.create_table()
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
        conn.commit()
        cursor.close()
        conn.close()

    def check_user_registered(self, username):
        self.create_table()
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE username=(?)''', (username,))
        result = cursor.fetchone() is not None
        conn.commit()
        cursor.close()
        conn.close()
        return result
        # returns true or false

    def update_username(self, new_username, old_username):
        self.create_table()
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''UPDATE users SET username=(?) WHERE username=(?)''', (new_username, old_username))
        conn.commit()
        cursor.close()
        conn.close()

    def try_login(self, username, password):
        self.create_table()
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE username=(?) AND password=(?)''', (username, password))
        result = cursor.fetchone() is not None
        cursor.close()
        conn.commit()
        conn.close()
        return result

class ScoresDB:
    def __init__(self):
        self.database = 'scores.db'

    def connect_to_db(self):
        conn = sqlite3.connect(self.database)
        return conn

    def create_table(self):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                username TEXT PRIMARY KEY NOT NULL, 
                score_json TEXT,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

    def insert_score(self, username, score):
        self.create_table()
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO scores (username, score_json) VALUES (?, ?)''', (username, score))
        conn.commit()
        cursor.close()
        conn.close()

    def check_user_registered(self, username):
        self.create_table()
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE username=(?)''', (username,))
        result = cursor.fetchone() is not None
        conn.commit()
        cursor.close()
        conn.close()
        return result
        # returns true or false

    def update_username(self, new_username, old_username):
        self.create_table()
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''UPDATE users SET username=(?) WHERE username=(?)''', (new_username, old_username))
        conn.commit()
        cursor.close()
        conn.close()

    def try_login(self, username, password):
        self.create_table()
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE username=(?) AND password=(?)''', (username, password))
        result = cursor.fetchone() is not None
        cursor.close()
        conn.commit()
        conn.close()
        return result


class Message:

    def __init__(self):
        self.username = ''
        self.password = ''
        self.database = UsersDB()
    
    def decode_json(self, data):
        try:
            decoded_data = data.decode()
            if decoded_data:
                return json.loads(decoded_data)
            else:
                # Handle the case when the decoded data is empty
                return None
        except json.decoder.JSONDecodeError as e:
            # Handle the invalid JSON case
            print(f"Error decoding JSON: {e}")
            return None
        
    def encode_json(self, data):
        try:
            json_data = json.dumps(data)
            return json_data.encode()
        except json.decoder.JSONDecodeError as e:
            # Handle the invalid JSON case
            print(f"Error decoding JSON: {e}")
            return None
        

class Sorting_Numbers:
    def __init__(self):
        self.numbers_to_sort = []
    
    def generate_numbers(self):
        numbers_to_sort = random.sample(range(1, 10), 5)
        random.shuffle(numbers_to_sort)
        self.numbers_to_sort = numbers_to_sort
        return numbers_to_sort
