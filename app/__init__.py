 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import os
from flask import Flask, render_template, redirect, request, session, flash
from database import register_user, login_user, init_db, logout_user, flowerbase, stats, stats_edit, garden, get_garden, garden_add, garden_pick, garden_water, seeds_use, profile, get_flower, purchase, flower_score, magic_power, buy, only_seeds, get_stats, get_profile
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

    # Access flower score + magic power
    user = session['username']
    fs = flower_score(user)
    mp = magic_power(user)
    return render_template('home.html', fs=fs, mp=mp)

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

@app.route('/garden', methods=['GET', 'POST'])
def garden():
    if 'username' not in session:
        return redirect('/login')

    user = session['username']
    if request.method == 'POST':
        if request.form.get('flower'):
            data = request.form['flower'].split('###')
            id = data[0]
            flower_id = data[1]
            flower_type = data[2]
            # print("buy flower:",flower_type)
            # print("buy id: ",id)
            garden_add(user, id, flower_type)
        if request.form.get('water'):
            id = request.form['water']
            garden_water(user, id)
        if request.form.get('pick'):
            id = request.form['pick']
            garden_pick(user, id)
    garden_info = get_garden(user)
    flower_info = get_flower()
    flower_info = only_seeds(flower_info, user)

    # Access flower score + magic power
    user = session['username']
    fs = flower_score(user)
    mp = magic_power(user)
    return render_template('garden.html', garden_info=garden_info, flower_info=flower_info, fs=fs, mp=mp)

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        # flash('post')
        return game_function()
        # return render_template('game.html', eq1=eq1, eq2=eq2, eq3=eq3)
    eq1, eq2, eq3 = rand_addition(), rand_addition(), rand_addition()

    # Access flower score + magic power
    user = session['username']
    fs = flower_score(user)
    mp = magic_power(user)
    return render_template('game.html', eq1=eq1, eq2=eq2, eq3=eq3, fs=fs, mp=mp)

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        # buy(session['username'], 1)
        return purchase()
    info = get_flower()

    # Access flower score + magic power
    user = session['username']
    fs = flower_score(user)
    mp = magic_power(user)
    return render_template('shop.html', info = info, fs=fs, mp=mp)

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/login')

    stats = get_stats()
    profile = get_profile()

    print("stats", stats)
    print("profile", profile)

    user = session['username']
    fs = flower_score(user)
    mp = magic_power(user)
    return render_template('profile.html', fs=fs, mp=mp, stats=stats, profile=profile)

# Run
if __name__ == "__main__":
    app.debug = True
    app.run()
