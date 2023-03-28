import csv

import numpy as np

from colorama import init as init_colorama
from colorama import Fore
from colorama import Style
init_colorama()

denom = int(input("Denominator to check: "))
verbose = bool(int(input("Verbose (0/1): ")))

def func(x):
    if(x < denom/2):
        return 2*x
    else:
        return 2*(denom - x)
    
visited = [False] * (denom + 1)
smallest_unvisited = 0

def GetSmallestUnvisited():
    """Return true if new smallest unvisited point exists"""
    global smallest_unvisited
    for i in range(smallest_unvisited, len(visited)):
        if(not visited[i]):
            smallest_unvisited = i
            return True
    
    smallest_unvisited = -1
    return False

orbits = []

while(GetSmallestUnvisited()):
    this_pass = [smallest_unvisited]
    visited[smallest_unvisited] = True

    to_visit = func(this_pass[-1])
    while(not visited[to_visit]):
        this_pass.append(to_visit)
        visited[to_visit] = True
        to_visit = func(this_pass[-1])

    if(to_visit in this_pass):
        index = this_pass.index(to_visit)
        if(index == len(this_pass) - 1):
            print(f"{Fore.BLUE}Found fixed point {this_pass[-1]}/{denom}.{Style.RESET_ALL}")
        else:
            orbits.append(this_pass[index:])
            print(f"{Fore.GREEN}Found orbit of period {len(orbits[-1])}:{Style.RESET_ALL}")
            print(f"{orbits[-1]}")
    elif(verbose):
        print(f"{Fore.BLACK}Pass unsuccessful: {this_pass}, next {to_visit}{Style.RESET_ALL}")