 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import os, sqlite3

# database initialization

def init_db():
    """initialize db if none exists"""
    if not os.path.exists('user_info.db'):
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        # User table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

def register_user():
    return 1

def login_user():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     if not username or not password:
#         flash('fill all fields')
#         return redirect('/login')

#     with sqlite3.connect('user_info.db') as conn:
#         cur
    return 1