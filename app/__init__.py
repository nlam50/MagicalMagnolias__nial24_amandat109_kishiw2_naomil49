 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import os
from flask import Flask, render_template, session, redirect, request
from database import register_user, login_user

# Session
app = Flask(__name__)
app.secret_key = os.urandom(32)

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
        if request.form.get['register']:
            return register_user()
        if request.form.get['login']:
            return login_user()
        else:
            flash('form error')
    return render_template('login.html')

# Run
if __name__ == "__main__":
    app.debug = True
    app.run()
