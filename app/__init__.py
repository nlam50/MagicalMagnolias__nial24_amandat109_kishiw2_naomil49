 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import os
from flask import Flask, render_template, redirect, request, session, flash
<<<<<<< HEAD
from database import register_user, login_user, init_db, logout_user
from methods import rand_addition, list_string, game_function, purchase
=======
from database import register_user, login_user, init_db, logout_user, flowerbase, stats, stats_edit, garden, garden_add, garden_remove, garden_edit, seeds_edit, profile
from methods import rand_addition, list_string, game_function
>>>>>>> 7d095bc2e8fe1ac61919aa78275a806d38a198d2

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
    return render_template('garden.html')

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
    if request.method == 'POST':
        # purchase_info = request.form.get('purchase_info')
        return purchase()
    return render_template('shop.html')

# Run
if __name__ == "__main__":
    app.debug = True
    app.run()
