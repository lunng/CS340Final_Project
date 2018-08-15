import json
import os

def getAverages():
	json_files = os.listdir("./Players JSONS")
    #to do for loop for all players the json files need to n
	averages = {}
	counts = {}
	for file in json_files:
		with open("./Players JSONS/" + file, 'r') as f:
			# with open("./Players JSONS/Kareem_Abdul-Jabbar.json", 'r') as f:
			playerstore = json.load(f)
			
			if "Year" in playerstore:
				x = 0
				for i in range (0, len(playerstore["Year"])):
					if str(playerstore["Year"][i]) not in averages:
						averages[playerstore["Year"][i]] = []
						counts[playerstore["Year"][i]] = 0
						for index in playerstore:
							if index == "Team" or index == "Name" or index == "Year":
								continue
							tempword = playerstore[index][i]
							if tempword is None:
								continue 
							tempword = tempword.replace("-", "")
							if tempword is None or tempword == ".":
								continue
							try:
								averages[playerstore["Year"][i]].append(float(tempword))
							except ValueError:
								continue
					else:
						x = 0
						for index in playerstore:
							if index == "Team" or index == "Name" or index == "Year":
								continue
							tempword = playerstore[index][i]
							if tempword is None:
								continue 
							tempword = tempword.replace("-", "")
							if tempword is None or tempword == ".":
								continue
							try:
								averages[playerstore["Year"][i]][x] += float(tempword)
								print(tempword)
							except ValueError:
								continue
							
						counts[playerstore["Year"][i]] += 1
						
						
	print(averages)
	print(counts)
	
def main():
	getAverages()
	
main()