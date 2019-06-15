#!/usr/bin/env python3

import random

print("Content-Type: text/html")
print()
print("<h1>" + str(random.randint(0,10)) +"</h1>")
print("<img src='../dogs/" + str(random.randint(1,3)) +".jpg'>")
