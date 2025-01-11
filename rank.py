import csv
import argparse
import pathlib

parser = argparse.ArgumentParser()


parser.add_argument("source_file", type=str)

args = parser.parse_args()

source_file = pathlib.Path(args.source_file).resolve()


headers = []
votes = []

with open(source_file, newline='') as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='"') 
    first = True
    for row in r:
        if first:
            first = False
            headers = row[1:]
        else:
            votes.append(row[1:6])






for r in range(5):
    print("Round {}".format(r+1))

    counts = {}

    for t in votes[0]:
        counts[t] = 0

    for vote in votes:
        counts[vote[0]] += 1
    
    n = len(votes)
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
        print("{}: {}".format(count, counts[count]))
    
    
    
    if ma/n > 0.5:
        print("{} has won, with {} votes ({}%)".format(ka,ma, round(ma/n*100)))
        break
    else:
        for vote in votes:
            vote.pop(vote.index(ki))

    
