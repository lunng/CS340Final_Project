import matplotlib.pyplot as plt
import json
import os
import numpy as np
from matplotlib import rcParams, cycler
from matplotlib.lines import Line2D

#Example code from http://abhay.harpale.net/blog/python/how-to-plot-multicolored-lines-in-matplotlib/
def find_contiguous_colors(colors):
	# finds the continuous segments of colors and returns those segments
	segs = []
	curr_seg = []
	prev_color = ''
	for c in colors:
		if c == prev_color or prev_color == '':
			curr_seg.append(c)
		else:
			segs.append(curr_seg)
			curr_seg = []
			curr_seg.append(c)
		prev_color = c
	segs.append(curr_seg) # the final one
	return segs
 
def plot_multicolored_lines(x,y,colors):
	segments = find_contiguous_colors(colors)
	start= 0
	for seg in segments:
		end = start + len(seg)
		if end < len(x):
			l, = plt.gca().plot(x[start:end+1],y[start:end+1],lw=2,c=seg[0]) 
		else:
			l, = plt.gca().plot(x[start:end],y[start:end],lw=2,c=seg[0]) 
		start = end

def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list		
		
def getTeamColors(teamcolors):
	teamcolors["Toronto"] = "#ce1141"
	teamcolors["Phoenix"] = "#e56020"
	teamcolors["Milwaukee"] = "#00471b"
	teamcolors["L.A. Lakers"] = "#552583"
	teamcolors["Golden State"] = "#fdb927"
	teamcolors["Oklahoma City"] = "#007ac1"
	teamcolors["Orlando"] = "#c2ccd2"
	teamcolors["Philadelphia"] = "#006bb6"
	teamcolors["Denver"] = "#00285e"
	teamcolors["Detroit"] = "#ed174c"
	teamcolors["Memphis"] = "#6189b9"
	teamcolors["New York"] = "#f9a01b"
	teamcolors["Cleveland"] = "#6f263d"
	teamcolors["Boston"] = "#007a33"
	teamcolors["Atlanta"] = "#e03a3e"
	teamcolors["Brooklyn"] = "#000000"
	teamcolors["Charlotte"] = "#1d1160"
	teamcolors["Chicago"] = "#ce1141"
	teamcolors["Indiana"] = "#002d62"
	teamcolors["L.A. Clippers"] = "#ed174c"
	teamcolors["Miami"] = "#98002e"
	teamcolors["Minnesota"] = "#0c2340"
	teamcolors["New Orleans"] = "#002b5c"
	teamcolors["Portland"] = "#e03a3e"
	teamcolors["Sacramento"] = "#5a2d81"
	teamcolors["San Antonio"] = "#000000"
	teamcolors["Utah"] = "#f9a01b"
	teamcolors["Washington"] = "#002b5c"
	teamcolors["Seattle"] = "#ffc200"

def convertCat(categories):
	categories["GP"] = "Games Played"
	categories["GS"] = "Games Started"
	categories["MPG"] = "Minutes Per Game"
	categories["FG"] = "Field Goals"
	categories["threeP"] = "Three Pointers"
	categories["FT"] = "Free Throw Percentage"
	categories["RPG"] = "Rebounds Per Game"
	categories["APG"] = "Assists Per Game"
	categories["SPG"] = "Steals Per Game"
	categories["BPG"] = "Blocks Per Game"
	categories["PPG"] = "Points Per Game"

	
	
def playerPlot(player_dictionary, averages):
	teamcolors = {}
	categories = {}
	avg_years = averages[0]
	avg_stats = averages[1]
	convertCat(categories)
	getTeamColors(teamcolors)
	try:
		years = player_dictionary["Year"]
	except KeyError:
		return
	teams = player_dictionary["Team"]
	colors = []
	for i in range(0, len(player_dictionary["Year"])):
		if player_dictionary["Team"][i] in teamcolors:
			colors.append(teamcolors[player_dictionary["Team"][i]])
		else:
			colors.append("#bfbfbf")
	
	labels = []
	label_colors = []
	last_team_name = ""
	for team_name, color in zip(teams, colors):
		if last_team_name == team_name:
			continue
		else:
			labels.append(team_name)
			label_colors.append(color)
			last_team_name = team_name
	
	labels = Remove(labels)
	label_colors = Remove(label_colors)
	if not labels:
		return
	print(labels)
	print(label_colors)
	
	for title in player_dictionary:
		if title == "Year" or title == "Team" or title == "Name":
			continue
		y = player_dictionary[title]
		i = -1
		for index in y:
			i += 1
			try: 
				toAdd = index.strip('-*')
				y[i] = float(toAdd)
			except:
				y[i] = float('nan')
			
		try:
			y = np.array(player_dictionary[title])
			y = y.astype(np.float)
		except ValueError:
			continue
		# plt.plot(years, games_played)
		team_combo = zip(player_dictionary["Year"], player_dictionary["Team"])
		
		custom_lines =[]
		for color_choice in label_colors:
			custom_lines.append(Line2D([0], [0], color=color_choice, lw=2))
		if title == "threeP" or title == "FG" or title == "FT":
			custom_lines.append(Line2D([0], [0], color="black", lw=2))
			labels.append("League Average")
		ax = plt.axes()
		
		ax.legend(custom_lines, labels)
		if title == "threeP" or title == "FG" or title == "FT":
			labels = labels[:-1]
		ax.xaxis.set_major_locator(plt.MaxNLocator(7))
		plt.xlabel("Year")
		plt.ylabel(categories[title])
		heading = player_dictionary["Name"][0]
		heading += " Career " + categories[title]
		if title == "threeP" or title == "FG" or title == "FT":
			averageList = []
			year_index = 0
			list_index = 0
			for single_year in avg_years:
				if year_index < len(years) and single_year == years[year_index]:
					year_index += 1
					if title == "threeP":
						averageList.append(avg_stats["3P%"][list_index])
					elif title == "FG":
						averageList.append(avg_stats["FG%"][list_index])
					elif title == "FT":
						averageList.append(avg_stats["FT%"][list_index])
				list_index += 1
			print(averageList)
			difference = len(years)-len(averageList)
			for i in range(0,difference):
				averageList.append(float('nan'))
			plt.plot(years, averageList, color="black")
		plt.title(heading)
		plot_multicolored_lines(years,y,colors)
		save_file_name = "./chartsdir/" + player_dictionary["Name"][0] + title + ".png"
		plt.savefig(save_file_name, bbox_inches='tight')
		plt.clf()


def main():
	fp = open('./Players JSONS/Cadillac_Anderson.json', 'r')
	plots = os.listdir("./chartsdir")
	json_files = os.listdir("./Players JSONS")
	with open('./Averages.json', 'r') as avgfile:
		averages = json.load(avgfile)
		averages[0].reverse()
		for list in averages[1]:
			try:
				list.reverse()
			except:
				continue
		#to do for loop for all players the json files need to n
		for file in json_files:
			filename = "./Players JSONS/" + file
			with open(filename, 'r') as fp:
				player_dict = json.load(fp)

				playerPlot(player_dict, averages)


if __name__ == '__main__':
	main()