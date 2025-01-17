# Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

import random
from flask import session, request, redirect, flash, render_template
from database import inc_mp, type_to_name, flower_score, magic_power

def rand_addition():
    n1 = random.randint(10, 50)
    n2 = random.randint(10,50)
    sum = n1 + n2
    return[n1, n2, sum]

# turns string into lists of numbers, '['10, '4', '6']' -> [10, 4, 6]
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
    ans1, ans2, ans3 = request.form.get('eq1_ans'), request.form.get('eq2_ans'), request.form.get('eq3_ans')

    if not ans1 or not ans2 or not ans3:
        flash('fill out all fields!')
        user = session['username']
        fs = flower_score(user)
        mp = magic_power(user)
        return render_template('game.html', eq1=eq1, eq2=eq2, eq3=eq3, fs=fs, mp=mp)

    ans1, ans2, ans3 = int(ans1), int(ans2), int(ans3)

    # logic
    a = [
        (ans1 == eq1[2]),
        (ans2 == eq2[2]),
        (ans3 == eq3[2])
    ]
    # print('a', a)
    if a != [True, True, True]:
        flash("incorrect!")
    else:
        flash("correct!")
        inc_mp(1)
    return redirect('/game')

def profile_to_profile(profile):
    li = {}
    for item in profile:
        # print('item', item)
        k = li.keys()
        flower_type = item[1]
        # flower_id = int(item[1])
        # flower_type = type_to_name(flower_id)
        if flower_type in k:
            li[flower_type] = li[flower_type] + 1
        else:
            li[flower_type] = 1
    a = list(li.items())
    return a

