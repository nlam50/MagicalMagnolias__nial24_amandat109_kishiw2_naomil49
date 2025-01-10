# Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

import random

def rand_addition():
    n1 = random.randint(10, 50)
    n2 = random.randint(10,50)
    sum = n1 + n2
    print(n1, n2, sum)
    return[n1, n2, sum]

def list_string(list):
    list = list.split(',')
    del = []
    for item in list:
        item = item[0,-1].split(',')
        print("item", item)
        for n in item:
            
