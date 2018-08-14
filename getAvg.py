#!/usr/bin/env python
import json
import os.path

def getAverage(p, f):
	filename = p + f
	# define 2 parallel lists 
	catList = ['GP', 'GS', 'MPG', 'FG', 'threeP', 'FT', 'RPG', 'APG', 'SPG', 'BPG', 'PPG']
	avgList = []

	# open specific player's json data file and calculate avg stats
	with open(filename) as f:
		data = json.load(f)
	count = 0
	total = 0
	cur = 0
	for cur in range(0, 11):
		for i in data[catList[cur]]:
			i = str(i)
			i = i.replace('*','')
			total += float(i)
			count += 1
		avg = round(total*1.0 / count, 2)
		avgList.append(avg)
		total = 0
		count = 0
	f.close()

	# create a dic
	avg_dict = {}
	for i in range(len(avgList)):
		avg_dict[catList[i]] = avgList[i]
	print avg_dict
	f.close()
	string = json.dumps(avg_dict)
	newFileName = p + '_avg.json'
	try:
		file = open(newFileName, "w+")
	except FileNotFoundError:
		return
	file.write(string)
	file.close()


def main():
	# pass in the name of the player to generate avg stat
	# for eg, read 'Allen_Iverson.json' and write to 'Allen_Iverson_avg.json'
	p = 'Allen_Iverson'
	f = '.json'
	getAverage(p, f)

if __name__ == '__main__':
	main()


