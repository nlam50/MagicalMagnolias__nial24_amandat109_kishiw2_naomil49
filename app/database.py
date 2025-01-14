 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import sqlite3, os, csv
from flask import Flask, request, render_template, redirect, url_for, flash, session


app = Flask(__name__)
app.secret_key = os.urandom(32)

# database initialization

def init_db():
    """initialize db if none exists"""
    conn = sqlite3.connect('magnolia.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flower_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flower_type TEXT UNIQUE NOT NULL,
            cost INTEGER INTEGER NOT NULL,
            max_growth INTEGER NOT NULL,
            water_req INTEGER NOT NULL,
            img TEXT UNIQUE NOT NULL
        )
    ''')        
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            user TEXT UNIQUE NOT NULL,
            magicpower INTEGER NOT NULL,
            flowerscore INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS garden (
            user TEXT NOT NULL,
            id INTEGER NOT NULL,
            flower_type TEXT  NOT NULL,
            days_watered INTEGER NOT NULL,
            grid_row INTEGER NOT NULL,
            grid_col INTEGER NOT NULL,
            max_growth INTEGER NOT NULL
        )
    ''')   
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            user TEXT UNIQUE NOT NULL,
            flower_type TEXT UNIQUE NOT NULL,
            max_growth INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seeds (
            user TEXT NOT NULL,
            flower_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def database_connect():
    if not os.path.exists('magnolia.db'):
        init_db()
    conn = sqlite3.connect('magnolia.db')
    return conn

#Flower
def flowerbase(user):
    if not os.path.exists('magnolia.db'):
        try:
            conn = database_connect()
            with open('flower.csv') as csvfile:
                readn = csv.reader(csvfile)
                cursor = conn.cursor()
                for info in readn:
                    ID = info[0]
                    flower_type = info[1]
                    cost = info[2]
                    max_growth = info[3]
                    water_req = info[4]
                    img = info[5]
                    cursor.execute('INSERT INTO flower_base (ID, flower_type, cost, max_growth, water_req, img) VALUES (?, ?, ?, ?, ?, ?)', (ID, flower_type, cost, max_growth, water_req, img))
                    cursor.execute('INSERT INTO seeds (user, flower_id, quantity) VALUES (?, ?, ?)', (user, ID, 0))
                    print("wa")
                conn.commit()
        except sqlite3.IntegrityError:
            flash('Database Error')
    else:
        print("database exists")
        
 
 #Stats
def stats(user, magicpower, flowerscore):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO stats (user, magicpower, flowerscore) VALUES (?, ?, ?)', (user, magicpower, flowerscore))
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')
 
def stats_edit(user, magicpower, flowerscore):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE stats SET magicpower = ? AND flowerscore = ? WHERE user = ?', (magicpower, flowerscore, user))
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')


#Garden
def garden(user):
    try:
        conn = database_connect()
        for r in range(6):
            for c in range(6):
                cursor = conn.cursor()
                cursor.execute('INSERT INTO garden (user, id, flower_type, days_watered, grid_row, grid_col, max_growth) VALUES (?, ?, ?, ?, ?, ?, ?)', (user, 0, "none", 0, r, c, 0))
        conn.commit()
    except sqlite3.IntegrityError:
        flash('Database Error')
    print("gardenrun")
        
def garden_add(user, r, c, ID, flower_type, max_growth):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE garden SET id = ? AND flower_type = ? AND max_growth = ? WHERE user = ? AND grid_row = ? AND grid_col = ?', (ID, flower_type, max_growth, user, r, c))
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')
    print("gardenrun")

        
def garden_edit(user, r, c, ID, days_watered):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE garden SET days_watered = ? WHERE user = ? AND grid_row = ? AND grid_col = ? AND id = ?', (days_watered, user, r, c, ID))
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')
    print("gardenrun")


#Profile
def profile(user, flower_type, max_growth):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO profile (user, flower_type, max_growth) VALUES (?, ?, ?)', (user, flower_type, max_growth))
        conn.commit()
    except sqlite3.IntegrityError:
        flash('Database Error')


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

# Game
def inc_mp(n):
    username = session['username']
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE stats SET magicpower = magicpower + ? WHERE user = ?', (n, username))
    except sqlite3.IntegrityError:
        flash('error')