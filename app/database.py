 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import os, sqlite3
from flask import request, redirect, render_template, flash

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
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('fill all fields')
        return redirect('/login')

    with sqlite3.connect('user_info.db') as conn:
        cursor = conn.cursor()
        # q = 'SELECT password FROM users WHERE username = ? (' + username + ',)'
        # cursor.execute(q)
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user_pass = cursor.fetchone()

        if user_pass:
            if user_pass[0] == password:
                session['username'] = username
                flash('logged in')
                return redirect('/')
        else:
            flash('invalid credentials')
    return redirect('/login')