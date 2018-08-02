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

#returns links to all the pages that have player names
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

######################################################################
# Parses player career statistic tables from wiki using beautiful soup
# following medium.com tutorial         REGULAR SEASON
######################################################################
def getPlayerStats():
    print ("###########################################")
    dwade_url = requests.get('https://en.wikipedia.org/wiki/Dwyane_Wade').text
    #creating parse tree to extract data from HTML
    soup = BeautifulSoup(dwade_url,'lxml')
    #should print page html
    #print(soup.prettify())
    #under wikisortable are the tables catergory names like year, team, etc.
    My_table = soup.find('table',{'class':'wikitable sortable'})
    #links will contain the titles(catergory name) in them
    links = My_table.findAll('a')
    #links
    #creating a dictionary
    Teams = []
    for link in links:
        Teams.append(link.get('title'))
    #should print multiple Miami, then Chicago, then Cleveland
    print(Teams)








def main():
	wiki = "https://en.wikipedia.org/w/api.php?"
	tutorial = 'http://econpy.pythonanywhere.com/ex/001.html'

	#Page that I used to write this code: https://medium.com/@stewynxavier/web-scraping-wiki-tables-using-beautifulsoup-and-python-6b9ea26d8722

	#wikiURL = searchWikiURL(wiki, 'NBA Players', '10')
	#wikiURL = queryWikiURL(wiki, ['Computer', 'Computer Science'])
	wikiURL = 'https://en.wikipedia.org/wiki/Lists_of_National_Basketball_Association_players'
	print(wikiURL)

	links = getLinks(wikiURL)


	print(links)


	#https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=xml&titles=Scott%20Aaronson
	#https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=xml&titles=List%20of%20computer%20scientists

	#urls = root.xpath('/SearchSuggestion/Section/Item/Text/text()')

	#print(urls)


if __name__ == '__main__':
	main()
getPlayerStats()
