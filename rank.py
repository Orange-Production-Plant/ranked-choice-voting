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
parser.add_argument("-n", "--num-winners", type=int, default=1)



args = parser.parse_args()

source_file = pathlib.Path(args.source_file).resolve()
skip_cols = args.skip
num_cols = args.columns
num_winners = args.num_winners



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


# droop quota
quota = n / (num_winners + 1)



num_winners_declared = 0
final_winners = [""]*num_winners
final_winner_votes = [0]*num_winners
final_winner_percentages = [0]*num_winners


def eliminate(votes, target):
    new_votes = []
    for vote in votes:
        try:
            vote.remove(target)
        except:
            pass
        if (len(vote) > 0):
            new_votes.append(vote)
        else:
            votes.remove(vote)

# random vote redistribution
def redistribute(votes, target, quota):
    random.shuffle(votes)

    # delete sufficient votes
    for vote in votes:
        if vote[0] == target:
            votes.remove(vote)
            quota -= 1
        
        if quota == 0:
            break
    
    # the remainder just eliminates that option
    eliminate(votes, target)
            

for r in range(num_cols):
    print("Round {}:".format(r+1))

    counts = {}
    # count up current first-rank votes for each option
    for vote in votes:
        if vote[0] in counts.keys():
            counts[vote[0]] += 1
        else:
            counts[vote[0]] = 1

    # print current vote status
    for key in counts.keys():    
        print("{}: {} ({}%)".format(key, counts[key], round(counts[key]/n*100)))
    

    lastoption = ""
    
    # find biggest winners, pick them out if over quota, then eliminate biggest loser
    for option, count in sorted(counts.items(), key=lambda x : x[1], reverse=True):
        if count > quota:
            print('"{}" has won, with {} votes ({}%)'.format(option, count, round(count/n*100)))
            
            redistribute(votes, option, maths.floor(quota) + 1)
            
            final_winners[num_winners_declared] = option
            final_winner_votes[num_winners_declared] = count
            final_winner_percentages[num_winners_declared] = round(count/n*100)
            num_winners_declared += 1
        
        lastoption = option

    if num_winners_declared == num_winners:
        break
    
    print('"{}" is the biggest loser, and will be removed'.format(lastoption))
    eliminate(votes, lastoption)

    print("")

print("")


if (num_winners_declared < num_winners):
    print("Insufficient winners were found. These options achieved the threshold: ")

for i in range(num_winners_declared):
    print("\"{}\" won, and achieved {} votes ({}%)".format(final_winners[i], final_winner_votes[i], final_winner_percentages[i]))