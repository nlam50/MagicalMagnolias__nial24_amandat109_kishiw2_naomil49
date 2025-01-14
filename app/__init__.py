 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import os
from flask import Flask, render_template, redirect, request, session, flash
from database import register_user, login_user, init_db, logout_user
from methods import rand_addition, list_string, game_function

# Session
app = Flask(__name__)
app.secret_key = os.urandom(32)

init_db()

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

@app.route('/shop')
def shop():
    return render_template('shop.html')

# Run
if __name__ == "__main__":
    app.debug = True
    app.run()
