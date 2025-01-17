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
            img TEXT UNIQUE NOT NULL,
            min_days INTEGER NOT NULL
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
            days_since_watered INTEGER NOT NULL,
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
                    days = info[6]
                    cursor.execute('INSERT INTO flower_base (ID, flower_type, cost, max_growth, water_req, img, min_days) VALUES (?, ?, ?, ?, ?, ?, ?)', (ID, flower_type, cost, max_growth, water_req, img, days))
                conn.commit()
        except sqlite3.IntegrityError:
            flash('Database Error')
    else:
        print("database exists")


 #Stats

def stats(user, magicpower, flowerscore, days):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO stats (user, magicpower, flowerscore, day) VALUES (?, ?, ?, ?)', (user, magicpower, flowerscore, days))
        print("stats successs")
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')

def stats_edit(user, magicpower, flowerscore):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE stats SET magicpower = ?, flowerscore = ? WHERE user = ?', (magicpower, flowerscore, user))
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
                print("garden success")
        test = cursor.execute('SELECT * FROM garden').fetchall()
        print("garden setup:",test)
        conn.commit()
    except sqlite3.IntegrityError:
        flash('Database Error')

def get_garden(user):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM garden WHERE user = ?', (user,)).fetchall()
        return result
    except sqlite3.IntegrityError:
        flash('Database Error')

def garden_add(user, ID, flower_type):
    try:
        print("info", user, ID, flower_type)
        conn = database_connect()
        cursor = conn.cursor()
        max = cursor.execute('SELECT max_growth FROM flower_base WHERE flower_type = ?', (flower_type,)).fetchone()
        print('max', max)
        max = max[0]
        print("garden_add: FLOWER_TYPE: ",flower_type)
        pretest = cursor.execute('SELECT * FROM garden WHERE user = ? AND id = ?', (user, ID,)).fetchone()
        print("PREtest: ",pretest)

        cursor.execute('UPDATE garden SET flower_type = ?, days_since_watered = ?, max_growth = ? WHERE user = ? AND id = ?', (flower_type, 1, max, user, ID))

        test = cursor.execute('SELECT * FROM garden WHERE user = ? AND id = ?', (user, ID,)).fetchone()
        print("test: ",test)
        databasetest = cursor.execute('SELECT * FROM garden').fetchall()
        print("POST-ADD database setup:",databasetest)
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')


def garden_water(user, ID):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        days_watered = cursor.execute('SELECT days_watered FROM garden WHERE user = ? AND id = ?', (user, ID,)).fetchone()
        days_watered = days_watered[0]
        days_since_watered = cursor.execute('SELECT days_since_watered FROM garden WHERE user = ? AND id = ?', (user, ID)).fetchone()
        days_since_watered = days_since_watered[0]
        max_growth = cursor.execute('SELECT max_growth FROM garden WHERE user = ? AND id = ?', (user, ID,)).fetchone()
        max_growth = max_growth[0]
        if(days_since_watered != 0 and days_watered != max_growth):
            print('d', days_watered)
            n = days_watered + 1
            cursor.execute('UPDATE garden SET days_watered = ? WHERE user = ? AND id = ?', (n, user, ID,))
            cursor.execute('UPDATE garden SET days_since_watered = ? WHERE user = ? AND id = ?', (0, user, ID,))
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')

def garden_pick(user, id):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        flower_type = cursor.execute('SELECT flower_type FROM garden WHERE user = ? AND id = ?', (user, id,)).fetchone()
        flower_type = flower_type[0]
        max_growth = cursor.execute('SELECT max_growth FROM garden WHERE user = ? AND id = ?', (user, id,)).fetchone()
        max_growth = max_growth[0]
        days = cursor.execute('SELECT days_watered FROM garden WHERE user = ? AND id = ?', (user, id,)).fetchone()
        days = days[0]
        if days != max_growth:
            cursor.execute('UPDATE garden SET flower_type = ?, days_watered = ?, days_since_watered = ?, max_growth = ? WHERE user = ? AND id = ?', ("none", 0, 0, 0, user, id))
            conn.commit()
            profile(user, flower_type, max_growth)
            seeds_use(user, flower_type)
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
                cursor.execute('INSERT INTO seeds (user, flower_id, quantity) VALUES (?, ?, ?)', (user, ID, 0,))
                print("seeds success")
            conn.commit()
    except sqlite3.IntegrityError:
            flash('Database Error')
    else:
        print("database exists")

def seeds_use(user, flower_id):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        quantity = cursor.execute('SELECT quantity FROM seeds WHERE user = ? AND flower_id = ?', (user, flower_id,)).fetchone()
        quantity = quantity[0] - 1
        cursor.execute('UPDATE seeds SET quantity = ? WHERE user = ? AND flower_id = ?', (quantity, user, flower_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')
    print("sed")

# filer list of all flower info into only the ones user has seeds for
def only_seeds(flower_info, user):
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            ids = cursor.execute('SELECT flower_id FROM seeds WHERE user = ? AND quantity > 0', (user,)).fetchall()
            print("only_seeds", ids)
            result = []
            for id in ids:
                id = id[0]
                print(id)
                info = cursor.execute('SELECT * FROM flower_base WHERE id = ?', (id,)).fetchall()
                print(info)
            return result
    except sqlite3.IntegrityError:
        flash('Database Error')


#Profile
def profile(user, flower_type, max_growth):
    try:
        conn = database_connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO profile (user, flower_type, max_growth) VALUES (?, ?, ?)', (user, flower_type, max_growth,))
        conn.commit()
    except sqlite3.IntegrityError:
        flash('Database Error !!')

def flower_score(user):
    try:
        with sqlite3.connect('magnolia.db')as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT flowerscore FROM stats WHERE user = ?', (user,)).fetchone()
            result = result[0]
            return result
    except sqlite3.IntegrityError:
        flash('Database Error')

def magic_power(user):
    try:
        with sqlite3.connect('magnolia.db')as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT magicpower FROM stats WHERE user = ?', (user,)).fetchone()
            result = result[0]
            return result
    except sqlite3.IntegrityError:
        flash('Database Error')

# User
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_pass')

    if not username or not password or not confirm_pass:
        flash('Please fill all fields')
    elif password != confirm_pass:
        flash('Password mismatch')
    else:
        try:
            with sqlite3.connect('magnolia.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
                conn.commit()
                stats(username, 1, 1, 0)
                garden(username)
                seeds(username)
                flash('User registered')
        except sqlite3.IntegrityError:
            flash('Username already exists')
    return redirect('/login')

def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please fill all fields')
        return redirect('/login')
    else:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            user_pass = cursor.fetchone()

            if user_pass:
                if user_pass[0] == password:
                    session['username'] = username
                    flash('Successfully logged in')
                    return redirect('/')
            else:
                flash('Invalid credentials')
    return redirect('/login')

def logout_user():
    session.pop('username',)
    flash('Logged out')
    return redirect('/login')


# Shop -> access flower db for info
def get_flower():
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT * FROM flower_base').fetchall()
            # print("RESULT",result)
            return result
    except sqlite3.IntegrityError:
        flash('Database error')

def purchase():
    purchase_info = request.form.get('purchase_info')
    purchase_info = purchase_info.split('###')
    # print(purchase_info)
    flower_id = int(purchase_info[0])
    cost = int(purchase_info[1])
    flower_type = purchase_info[2]
    username = session['username']

    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT magicpower, flowerscore FROM stats WHERE user = ?', (username,)).fetchone()
            magicpower = result[0]
            flowerscore = result[1]

            if flowerscore >= flower_id:
                if magicpower >= cost:
                    m = 'Purchased x1 ' + flower_type
                    flash(m)
                    buy(username, flower_id, 0)
                else:
                    flash('Not enough magic power. Play minigames to earn more!')
            else:
                # comment after, for testing purposes
                buy(username, flower_id, 0)
                flash('Flower not unlocked. Grow more flowers to increase flower score!')
    except sqlite3.IntegrityError:
        flash('Database error')
    return redirect('shop')

def buy(username, flower_id, cost):
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            quantity = cursor.execute('SELECT quantity FROM seeds WHERE user = ? AND flower_id = ?', (username,flower_id)).fetchone()
            if not quantity:
                quantity = 0
                cursor.execute('INSERT INTO seeds (user, flower_id, quantity) VALUES (?, ?, 0)', (username, flower_id,))
            else:
                quantity = quantity[0]
            cursor.execute('UPDATE seeds SET quantity = ? WHERE user = ? AND flower_id = ?', (quantity + 1, username, flower_id))
            cursor.execute('UPDATE stats SET magicpower = magicpower - ? WHERE user = ?', (cost, username))
    except sqlite3.IntegrityError:
        flash('Database error')

# Game
def inc_mp(n):
    username = session['username']
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE stats SET magicpower = magicpower + ? WHERE user = ?', (n, username))
    except sqlite3.IntegrityError:
        flash('Database error')
