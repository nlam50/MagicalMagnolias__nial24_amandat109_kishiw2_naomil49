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
            flowerscore INTEGER NOT NULL,
            day INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS garden (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            flower_type TEXT NOT NULL,
            days_watered INTEGER NOT NULL,
            day_last_watered INTEGER NOT NULL,
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
def flowerbase():
    if not os.path.exists('magnolia.db'):
        print("wa")
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
                cursor.execute('INSERT INTO garden (user, flower_type, days_watered, days_since_watered, max_growth) VALUES (?, ?, ?, ?, ?)', (user, "none", 0, 0, 0))
        conn.commit()
    except sqlite3.IntegrityError:
        flash('Database Error')

def get_garden(user):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM garden WHERE user = ?', (user)).fetchall()
    except sqlite3.IntegrityError:
        flash('Database Error')

def garden_add(user, ID, flower_type):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        max_growth = cursor.execute('SELECT max_growth FROM flower_base WHERE flower_type = ?', (flower_type)).fetchone()
        cursor.execute('UPDATE garden SET flower_type = ? AND max_growth = ? WHERE user = ? AND id = ?', (flower_type, max_growth, user, ID))
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')

def garden_water(user, ID):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        days_watered = cursor.execute('SELECT days_watered FROM garden WHERE user = ? AND id = ?', (user, ID)).fetchone()
        days_since_watered = cursor.execute('SELECT days_since_watered FROM garden WHERE user = ? AND id = ?', (user, ID)).fetchone()
        max_growth = cursor.execute('SELECT max_growth FROM garden WHERE user = ? AND id = ?', (user, ID)).fetchone()
        if(days_since_watered != 0 and days_watered != max_growth):
            cursor.execute('UPDATE garden SET days_watered = ? WHERE user = ? AND id = ?', (days_watered + 1, user, ID))
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')

def garden_pick(user, id):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        flower_type = cursor.execute('SELECT flower_type FROM garden WHERE user = ? AND id = ?', (user, id)).fetchone()
        max_growth = cursor.execute('SELECT max_growth FROM garden WHERE user = ? AND id = ?', (user, id)).fetchone()
        cursor.execute('UPDATE garden SET flower_type = ? AND days_watered = ? AND days_since_watered = ? AND max_growth = ? WHERE user = ? AND id = ?', ("none", 0, 0, 0, user, id))
        conn.commit()
        profile(user, flower_type, max_growth)
    except sqlite3.IntegrityError:
        print('Database Error')


#Seeds

def seeds(user):
    try:
        conn = database_connect()
        with open('flower.csv') as csvfile:
            readn = csv.reader(csvfile)
            cursor = conn.cursor()
            for info in readn:
                ID = info[0]
                cursor.execute('INSERT INTO seeds (user, flower_id, quantity) VALUES (?, ?, ?)', (user, ID, 0))
            conn.commit()
    except sqlite3.IntegrityError:
            flash('Database Error')
    else:
        print("database exists")

def seeds_use(user, flower_id):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        quantity = cursor.execute('SELECT quantity FROM seeds WHERE user = ? AND id = ?', (user, id)).fetchone()
        cursor.execute('UPDATE seeds SET quantity = ? WHERE user = ? AND flower_id = ?', (quantity, user, flower_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')
    print("sed")

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
                cursor.execute('INSERT INTO stats (user, magicpower, flowerscore, day) VALUES (?,?,?,?)', (username, 1, 1, 1))
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
def get_flower():
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT * FROM flower_base').fetchall()
            return result
    except sqlite3.IntegrityError:
        flash('error')

def purchase():
    purchase_info = request.form.get('purchase_info')
    purchase_info = list(map(int, purchase_info.split('###')))
    id = purchase_info[0]
    cost = purchase_info[1]
    username = session['username']

    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT magicpower, flowerscore FROM stats WHERE user = ?', (username,)).fetchone()
            magicpower = result[0]
            flowerscore = result[1]

            if flowerscore >= id:
                if magicpower >= cost:
                    flash('user can buy')
                else:
                    flash('not enough magic power. play minigames to earn more!')
            else:
                flash('flower not unlocked')
    except sqlite3.IntegrityError:
        flash('error')
    return redirect('shop')

# Game
def inc_mp(n):
    username = session['username']
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE stats SET magicpower = magicpower + ? WHERE user = ?', (n, username))
    except sqlite3.IntegrityError:
        flash('error')
