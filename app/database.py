 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import os, sqlite3
from flask import request, redirect, render_template, flash, session


def flowerbase(): 
    try:
        with open('flower.csv') as conn:
            read = csv.reader(conn)
            for info in read:
                ID = info[0]
                flower_type = info[1]
                cost = info[2]
                max_growth = info[3]
                water_req = info[4]
                img = info[5]
    except sqlite3.IntegrityError:
        flash('Database Error')
        
# database initialization
def init_db():
    """initialize db if none exists"""
    if not os.path.exists('magnolia.db'):
        conn = sqlite3.connect('magnolia.db')
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

# User
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_pass')

    if not username or not password or not confirm_pass:
        flash('fill all fields')
    elif password != confirm_pass:
        flash('passwords dont match')
    else:
        try:
            with sqlite3.connect('magnolia.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
                conn.commit()
                flash('registered')
        except sqlite3.IntegrityError:
            flash('username already exists')
    return redirect('/login')

def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('fill all fields')
        return redirect('/login')
    else:
        with sqlite3.connect('magnolia.db') as conn:
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

def logout_user():
    session.pop('username',)
    flash('logged out')
    return redirect('/login')
        
# Shop -> access flower db for info
def flower_info():
    return [1]