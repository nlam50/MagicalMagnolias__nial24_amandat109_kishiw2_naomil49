# Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

import random
from flask import request, redirect, flash, render_template

def rand_addition():
    n1 = random.randint(10, 50)
    n2 = random.randint(10,50)
    sum = n1 + n2
    return[n1, n2, sum]

# turns string into lists of numbers
def list_string(n):
    n = n.split('###')
    li = []
    for item in n:
        int_list = list_string2(item)
        li.append(int_list)
    return li

def list_string2(li):
    x = li[1:-1]
    x = x.split(', ')
    x = list(map(int, x))
    return(x)

def game_function():
    # get prior equation info
    eq_info = list_string(request.form.get('eq_info'))
    eq1, eq2, eq3 = eq_info[0], eq_info[1], eq_info[2]
    ans1, ans2, ans3 = int(request.form.get('eq1_ans')), int(request.form.get('eq2_ans')), int(request.form.get('eq3_ans'))

    if not ans1 or not ans2 or not ans3:
        flash('fill out all fields!')
        return render_template('game.html', eq1=eq1, eq2=eq2, eq3=eq3)

    # logic
    a = [
        (ans1 == eq1[2]),
        (ans2 == eq2[2]),
        (ans3 == eq3[2])
    ]
    print('a', a)
    if a != [True, True, True]:
        flash("incorrect!")
    else:
        flash("correct!")
    return redirect('/game')