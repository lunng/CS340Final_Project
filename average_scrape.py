import os
import sys
from bs4 import BeautifulSoup
from lxml import etree, objectify
from pathlib import Path 
import requests
import json
import csv
import copy
import collections

header = {
    'User-Agent': 'Gray Lunn',
    'From': 'lunng@oregonstate.edu',
	'Class_Title' : 'CS340'
}

def setAction(whatAction):
	return 'action='+whatAction+'&'

def setFormat(whatFormat):
	return 'format='+whatFormat+'&'

def searchFor(searchTerms, limit):
	return 'search='+searchTerms+'&limit='+limit+'&'

def titles(whatTitles):
	listOfTitles = ''
	for title in whatTitles:
		listOfTitles += title+"|"
	return 'titles='+listOfTitles[:-1]+'&'

def getPage(url):
	#use the header to identify user to wikimedia servers
	page = requests.get(url, header).text
	return page

def searchWikiURL(wikiURL, searchTerms, limit):
	return wikiURL+setAction('opensearch')+setFormat('xml')+searchFor(searchTerms, limit)

def queryWikiURL(wikiURL, queryTerms):
	return wikiURL+setAction('query')+setFormat('xml')+titles(queryTerms)
	
	
def pp(e):
    print(etree.tostring(e, pretty_print=True))
    print('')

def strip_ns(tree):
    for node in tree.iter():
        try:
            has_namespace = node.tag.startswith('{')
        except AttributeError:
            continue
        if has_namespace:
            node.tag = node.tag.split('}', 1)[1]

def getLinks(wikiURL):
	rawPage = getPage(wikiURL)
	
	soup = BeautifulSoup(rawPage, 'lxml')
	#print(soup.prettify())
	
	myList = soup.find('div', {'class':'toc'})
	
	unformatted_links = myList.find_all('a')
	
	links = []
	for link in unformatted_links:
		links.append(link.get('href'))
	return links
	
def getPlayers(link):
	wiki = 'https://en.wikipedia.org'
	wikiURL = wiki + link
	rawPage = getPage(wikiURL)
	
	soup = BeautifulSoup(rawPage, 'lxml')
	
	lists = soup.find_all('div', {'class':'columns'})
	links = []
	
	for myList in lists:
		unformatted_links = myList.find_all('a')
		for link in unformatted_links:
			links.append(link.get('href'))
	
	print(links)
	return links
	
def getPlayerName(soup):

	title = soup.find('h1', {"id": "firstHeading"})
	print(title.text)
	
	return title.text

# gets career stats for a single player  
def getStats(link):
	#print(link)
	wiki = 'https://en.wikipedia.org'
	wikiURL = wiki + link  
	rawPage = getPage(wikiURL)
	soup = BeautifulSoup(rawPage, 'lxml')
	table_classes = {"class": ["sortable", "plainrowheaders"]}
	

	# finds first sortable table (which is reg season stats table)
	Tables = soup.find_all("table", table_classes)
	try:
		regSeasonTable = Tables[0]
	except IndexError:
		return {}
	
	# Lists to store stats for each category 
	Year = []
	Team = []
	GP = []
	GS = []
	MPG = []
	FG = []
	threeP = []
	FT = []
	RPG = []
	APG = []
	SPG = []
	BPG = []
	PPG = []


	for row in regSeasonTable.find_all("tr"):	
		cells = row.find_all("td")
		if len(cells) == 13:
			Year.append(cells[0].find(text=True))
			Team.append(cells[1].find(text=True))
			GP.append(cells[2].find(text=True))
			GS.append(cells[3].find(text=True))
			MPG.append(cells[4].find(text=True))
			FG.append(cells[5].find(text=True))
			threeP.append(cells[6].find(text=True))
			FT.append(cells[7].find(text=True))
			RPG.append(cells[8].find(text=True))
			APG.append(cells[9].find(text=True))
			SPG.append(cells[10].find(text=True))
			BPG.append(cells[11].find(text=True))
			PPG.append(cells[12].find(text=True))
			
	#playoffsTable = soup.find_all("table", table_classes)[1]

	# AllStats = []
	# AllStats.append(Year)
	# AllStats.append(Team)
	# AllStats.append(GP)
	# AllStats.append(GS)
	# AllStats.append(MPG)
	# AllStats.append(FG)
	# AllStats.append(threeP)
	# AllStats.append(FT)
	# AllStats.append(RPG)
	# AllStats.append(APG)
	# AllStats.append(SPG)
	# AllStats.append(BPG)
	# AllStats.append(PPG)
		
	AllStats = {}
	AllStats['Year'] = Year
	AllStats['Team'] = Team
	AllStats['GP'] = GP
	AllStats['GS'] = GS
	AllStats['MPG'] = MPG
	AllStats['FG'] = FG
	AllStats['threeP'] = threeP
	AllStats['FT'] = FT
	AllStats['RPG'] = RPG
	AllStats['APG'] = APG
	AllStats['SPG'] = SPG
	AllStats['BPG'] = BPG
	AllStats['PPG'] = PPG

	for stats in AllStats:
		i = 0 
		for stat in AllStats[stats]:
			if isinstance(AllStats[stats][i], str):
				AllStats[stats][i] = AllStats[stats][i].replace("\u2013", "-")
				AllStats[stats][i] = AllStats[stats][i].replace("\n", "-")
			i += 1

	return [AllStats, soup]	
	
	
def statsToFile(stats, player, name):
	name = name.replace("(basketball)", "")
	list_item = []
	list_item.append(name)
	stats["Name"] = list_item
	string = json.dumps(stats)
	filename = "./Players JSONS/"
	filename += player + ".json"
	filename = filename.replace("/wiki/", "")
	filename = filename.replace("/w/index.php?title=", "")
	filename = filename.replace("_(basketball)&action=edit&redlink=1", "")
	filename = filename.replace("_(basketball)", "")
	print(filename)
	try:
		file = open(filename, "w+")
	except FileNotFoundError:
		return
	file.write(string)
	file.close()
	
def getAverages():
	with open('./Averages.csv', 'r', encoding = 'utf8') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		header = next(spamreader)
		print(header)
		rowCount = 0
		years = []
		stats_by_year = {}
		for attributeName in header:
			stats_by_year[attributeName] = []
		for row in spamreader:
			headerIndex = 0
			#This is one way to iterate through all of the attribute columns with their corresponding headers
			for attributeName in header:
				tempvar=row[headerIndex]
				if headerIndex == 1:
					years.append(tempvar)
				if headerIndex == 23:
					try:
						stats_by_year[attributeName].append(float(tempvar))
					except:
						stats_by_year[attributeName].append(float('nan'))
				if headerIndex == 24:
					try:
						stats_by_year[attributeName].append(float(tempvar))
					except:
						stats_by_year[attributeName].append(float('nan'))				
				if headerIndex == 25:
					try:
						stats_by_year[attributeName].append(float(tempvar))
					except:
						stats_by_year[attributeName].append(float('nan'))
								#print('\t' + row[headerIndex])
								

				headerIndex += 1
		print(years)
		print("len(fg%)")
		print(len(stats_by_year['FG%']))
		print(len(years))
		print(stats_by_year)
		all_info = []
		all_info.append(years)
		all_info.append(stats_by_year)
		json_str = json.dumps(all_info)
		with open('./Averages.json', 'w+', encoding = 'utf8') as averages:
			averages.write(json_str)
			
def main():
	getAverages()
			

	#print(links)
	#print()
	#print(players)

	#https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=xml&titles=Scott%20Aaronson
	#https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=xml&titles=List%20of%20computer%20scientists
	
	#urls = root.xpath('/SearchSuggestion/Section/Item/Text/text()')

	#print(urls)


if __name__ == '__main__':
	main()