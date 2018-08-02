import os
import sys
from bs4 import BeautifulSoup
from lxml import etree, objectify
import requests

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
	
	unformatted_links = myList.findAll('a')
	
	links = []
	for link in unformatted_links:
		links.append(link.get('href'))
	return links
	
def getPlayers(link):
	wiki = 'https://en.wikipedia.org'
	wikiURL = wiki + link
	rawPage = getPage(wikiURL)
	
	soup = BeautifulSoup(rawPage, 'lxml')
	
	myList = soup.find('div', {'class':'columns'})
	
	links = []
	

	unformatted_links = myList.findAll('a')
	for link in unformatted_links:
		links.append(link.get('href'))
			
	return links

# gets career stats for a single player  
def getStats(link):
	#print(link)
	wiki = 'https://en.wikipedia.org'
	wikiURL = wiki + link  
	rawPage = getPage(wikiURL)
	soup = BeautifulSoup(rawPage, 'lxml')
	table_classes = {"class": ["sortable", "plainrowheaders"]}
	

	# finds first sortable table (which is reg season stats table)
	regSeasonTable = soup.findAll("table", table_classes)[0]
	
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

	for row in regSeasonTable.findAll("tr"):	
		cells = row.findAll("td")
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
			
	#playoffsTable = soup.findAll("table", table_classes)[1]

	Year = [x.encode('UTF8') for x in Year]
	Team = [x.encode('UTF8') for x in Team]
	GP = [x.encode('UTF8') for x in GP]
	GS = [x.encode('UTF8') for x in GS]
	MPG = [x.encode('UTF8') for x in MPG]
	FG = [x.encode('UTF8') for x in FG]
	threeP = [x.encode('UTF8') for x in threeP]
	FT = [x.encode('UTF8') for x in FT]
	RPG = [x.encode('UTF8') for x in RPG]
	APG = [x.encode('UTF8') for x in APG]
	SPG = [x.encode('UTF8') for x in SPG]
	BPG = [x.encode('UTF8') for x in BPG]
	PPG = [x.encode('UTF8') for x in PPG]

	print(GP) 

def main():
	wiki = "https://en.wikipedia.org/w/api.php?"
	tutorial = 'http://econpy.pythonanywhere.com/ex/001.html'
	
	#Page that I used to write this code: https://medium.com/@stewynxavier/web-scraping-wiki-tables-using-beautifulsoup-and-python-6b9ea26d8722

	#wikiURL = searchWikiURL(wiki, 'NBA Players', '10')
	#wikiURL = queryWikiURL(wiki, ['Computer', 'Computer Science'])
	wikiURL = 'https://en.wikipedia.org/wiki/Lists_of_National_Basketball_Association_players'
	#print(wikiURL)

	links = getLinks(wikiURL)
	players = getPlayers(links[0])
	

	#getStats(players[0])



	#print(links)
	#print()
	#print(players)

	#https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=xml&titles=Scott%20Aaronson
	#https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=xml&titles=List%20of%20computer%20scientists
	
	#urls = root.xpath('/SearchSuggestion/Section/Item/Text/text()')

	#print(urls)


if __name__ == '__main__':
	main()