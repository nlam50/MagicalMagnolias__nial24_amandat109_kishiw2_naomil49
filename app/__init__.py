 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import os
from flask import Flask, render_template, redirect, request, session, flash
from database import register_user, login_user, init_db, logout_user, flowerbase, stats, stats_edit, garden, get_garden, garden_add, garden_pick, garden_water, seeds_use, profile, get_flower, purchase
from methods import rand_addition, list_string, game_function

# Session
app = Flask(__name__)
app.secret_key = os.urandom(32)

flowerbase()

# Routing

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/login')
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If form info is from register, register the user; if info from login, user logs in
    if request.method == 'POST':
        if request.form.get('register'):
            return register_user()
        if request.form.get('login'):
            return login_user()
        else:
            flash('form error')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return logout_user()

@app.route('/garden')
def garden():
    if 'username' not in session:
        return redirect('/login')

    user = session['username']
    if request.method == 'POST':
        if request.form.get('flower'):
            data = request.form['flower'].split().strip()
            id = data[0]
            flower_id = data[1]
            flower_type = data[2]
            garden_add(user, id, flower_type)
            seeds_use(user, flower_id)
        if request.form.get('water'):
            id = request.form['water']
            garden_water(user, id)
        if request.form.get('pick'):
            id = request.form['pick']
            garden_water(user, id)
    garden_info = get_garden(user)
    print(garden_info)
    flower_info = get_flower()
    return render_template('garden.html', garden_info=garden_info, flower_info=flower_info)

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        # flash('post')
        return game_function()
        # return render_template('game.html', eq1=eq1, eq2=eq2, eq3=eq3)
    eq1, eq2, eq3 = rand_addition(), rand_addition(), rand_addition()
    return render_template('game.html', eq1=eq1, eq2=eq2, eq3=eq3)

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        return purchase()
    info = flower_info()
    return render_template('shop.html', info = info)

# Run
if __name__ == "__main__":
    app.debug = True
    app.run()
