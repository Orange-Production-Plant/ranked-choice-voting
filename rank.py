#!/bin/python3

import csv
import argparse
import pathlib

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





n = len(votes)
print("There are {} responses in total.\n".format(n))

is_winner_declared = False

final_winner = ""
final_winner_votes = 0
final_winner_percentage = 0

for r in range(num_cols):
    print("Round {}:".format(r+1))

    counts = {}
    for vote in votes:
        if vote[0] in counts.keys():
            counts[vote[0]] += 1
        else:
            counts[vote[0]] = 1
    
    ma = 0
    mi = n
    ka = ""
    ki = ""
    for count in counts.keys():    
        if counts[count] > ma:
            ma = counts[count]
            ka = count
        
        if counts[count] < mi:
            mi = counts[count]
            ki = count
        
        print("{}: {} ({}%)".format(count, counts[count], round(counts[count]/n*100)))
    
    if ma/n > 0.5:
        print('"{}" has won, with {} votes ({}%)'.format(ka,ma, round(ma/n*100)))
        is_winner_declared = True
        break
    else:
        print('"{}" is the biggest loser, and will be removed'.format(ki))
        for vote in votes:
            if ki in vote:
                vote.pop(vote.index(ki))
    
    final_winner = ka
    final_winner_votes = ma
    final_winner_percentage = round(ma/n*100)

    print("")
    


if (not is_winner_declared):
    print("No majority winner was found through ranked elimination.")
    print("A plurality was achieved by \"{}\", with {} votes ({}%).".format(final_winner, final_winner_votes,final_winner_percentage))
