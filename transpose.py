#!/bin/python3

import csv
import argparse
import pathlib
import re

parser = argparse.ArgumentParser()

parser.add_argument("skip", type=int)
parser.add_argument("columns", type=int)
parser.add_argument("source_file", type=str)
parser.add_argument("output_file", type=str)

args = parser.parse_args()

source_file = pathlib.Path(args.source_file).resolve()
output_file = pathlib.Path(args.output_file).resolve()
skip_cols = args.skip
num_cols = args.columns

raw_headers = []
votes = []

with open(source_file, newline='') as csvfile:
	r = csv.reader(csvfile, delimiter=',', quotechar='"') 
	first = True
	for row in r:
		if first:
			first = False
			raw_headers = row[skip_cols:skip_cols + num_cols]
		else:
			votes.append(row[skip_cols:skip_cols + num_cols])

num_votes = len(votes)

headers = []

choice_names = ("first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth")
choice_regexes = [re.compile(x, re.IGNORECASE) for x in choice_names]



# match any of "[" "]"
pattern = re.compile(R"[\[\]]")
for header in raw_headers:
	headers.append(pattern.split(header)[1])

new_votes = [[""]*num_cols]*num_votes

# if we find the "nth" (as in the ordinal name) in a vote, it means that it should go to position n in the final votes array
for i in range(num_votes):
	temp_vote_arr = [None] * num_cols
	for j in range(num_cols):
		for k in range(num_cols):
			if choice_regexes[k].search(votes[i][j]):
				temp_vote_arr[k] = headers[j]
	new_votes[i] = temp_vote_arr


for vote in new_votes:
	print(vote)

with open(output_file, "w", newline='') as csvfile:
	w = csv.writer(csvfile, delimiter=',', quotechar='"')
	w.writerow(raw_headers)
	w.writerows(new_votes)
