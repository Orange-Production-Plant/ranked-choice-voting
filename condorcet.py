#!/bin/python3

import csv
import argparse
import pathlib
import random
import math as maths

parser = argparse.ArgumentParser()

parser.add_argument("skip", type=int)
parser.add_argument("columns", type=int)
parser.add_argument("source_file", type=str)



args = parser.parse_args()

source_file = pathlib.Path(args.source_file).resolve()
skip_cols = args.skip
num_cols = args.columns



headers = []
votes = []


with open(source_file, newline='') as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='"') 
    first = True
    for row in r:
        if first:
            first = False
            headers = row[skip_cols:]
        else:
            votes.append(row[skip_cols:skip_cols + num_cols])

quota = len(votes) / 2 




n = len(votes)
print("There are {} responses in total.\n".format(n))

condorcet_winner = ""

potential_champions = votes[0].copy()


for i in range(num_cols):
    champion = potential_champions[i]
    print("'{}' is the champion!".format(champion))

    is_condorcet_winner = True
    for j in range(i+1, len(potential_champions)):
        challenger = potential_champions[j]
        print("Facing off against: '{}'".format(challenger))
        champion_wins = 0
        for vote in votes:
            for option in vote:
                if option == champion:
                    champion_wins += 1
                    break
                elif option == challenger:
                    break
        
        if champion_wins < quota:
            print("Champion was defeated by {}, with only {} wins.".format(challenger, champion_wins))
            is_condorcet_winner = False
            break
        elif champion_wins == quota:
            print("Champion and challenger knocked one another out!")
            is_condorcet_winner = False
            try:
                potential_champions.remove(challenger)
            except:
                pass
            break
        else:
            print("Champion won against challenger, with {} wins.".format(champion_wins))
    
    if (is_condorcet_winner):
        condorcet_winner = champion
        break

if (condorcet_winner != ""):
    print("The Condorcet winner is {}!".format(condorcet_winner))
else:
    print("No Condorcet winner was found!")