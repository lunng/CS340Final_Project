#whoosh http://whoosh.readthedocs.io/en/latest/quickstart.html
import whoosh
from whoosh.index import create_in
from whoosh.fields import*
from whoosh.qparser import QueryParser
import json
import os

def createIndex():
#what we're searching over
	schema = Schema(Year=TEXT(stored=True), Team=TEXT(stored=True), GP=TEXT(stored=True),
	GS=TEXT(stored=True), MPG=TEXT(stored=True), FG=TEXT(stored=True), threeP=TEXT(stored=True),
	FT=TEXT(stored=True), RPG=TEXT(stored=True),APG=TEXT(stored=True),SPG=TEXT(stored=True),
	BPG=TEXT(stored=True), PPG=TEXT(stored=True), Name=TEXT(stored=True),)

    #creates a Storage object to contain the index
	if not os.path.exists("indexdir"):
		os.mkdir("indexdir")
		
	ix = create_in("indexdir", schema)
	return ix

def openIndex():
	ix = index.open_dir("indexdir")
	return ix
	
def addToIndex(year, team, gp, gs, mpg, fg, threep, ft, rpg, apg, spg, bpg, ppg, name, ix): 

	writer = ix.writer()
	writer.add_document(Year= year, Team=team, GP=gp, GS=gs, MPG=mpg, FG=fg,
	threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg, Name=name)
	writer.commit()
	
    # writer.add_document(Year= year, Team=team, GP=gp, GS=gs, MPG=mpg, FG=fg,
    # threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg)


	
def queryIndex(queryType, queryValue, ix):
	with ix.searcher() as searcher:
		query = QueryParser(queryType, ix.schema).parse(queryValue)
		results = searcher.search(query, limit=None)
	
		for result in results:
			print(result)

# def indexing(year, team, gp, gs, mpg, fg, threep, ft, rpg, apg, spg, bpg, ppg, name):
    # #what we're searching over
	# schema = Schema(Year=TEXT(stored=True), Team=TEXT(stored=True), GP=TEXT(stored=True),
	# GS=TEXT(stored=True), MPG=TEXT(stored=True), FG=TEXT(stored=True), threeP=TEXT(stored=True),
	# FT=TEXT(stored=True), RPG=TEXT(stored=True),APG=TEXT(stored=True),SPG=TEXT(stored=True),
	# BPG=TEXT(stored=True), PPG=TEXT(stored=True), Name=TEXT(stored=True),)

    # #creates a Storage object to contain the index
	# if not os.path.exists("indexdir"):
		# os.mkdir("indexdir")
	# ix = create_in("indexdir", schema)

    # #ix = open_dir("index")
    # #writer() lets you add documents to the index.
	# writer = ix.writer()

	# writer.add_document(Year= year, Team=team, GP=gp, GS=gs, MPG=mpg, FG=fg,
	# threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg, Name=name)

    # # writer.add_document(Year= year, Team=team, GP=gp, GS=gs, MPG=mpg, FG=fg,
    # # threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg)

	# writer.commit()

    # #searching test
	# with ix.searcher() as searcher:
		# query = QueryParser("Year", ix.schema).parse("1969-70")
		# results = searcher.search(query, limit=None)

		# print("____________________________________________________________________")
	# # print("results:%s" % str(results)
		# for result in results:
			# print(result)

    # # {"title": u"First document", "path": u"/a"}

def method_1(ix):
	writer = ix.writer(procs=4, limitmb=2048)
	json_files = os.listdir("./Players JSONS")
    #to do for loop for all players the json files need to n
	for file in json_files:
		with open("./Players JSONS/" + file, 'r') as f:
    #with open("./Players JSONS/Kareem_Abdul-Jabbar.json", 'r') as f:
			playerstore = json.load(f)
			if "Year" in playerstore:
				year = ' '.join(playerstore["Year"]) #storing the string
			else:
				continue
			# print (playerstore["Team"])
			team = ' '.join(playerstore["Team"]) #storing the string

			# print (playerstore["GP"])
			gp = ' '.join(playerstore["GP"]) #storing the string

			# print (playerstore["GS"])
			gs = ' '.join(playerstore["GS"]) #storing the string

			# print (playerstore["MPG"])
			mpg = ' '.join(playerstore["MPG"]) #storing the string

			# print (playerstore["FG"])
			fg = ' '.join(playerstore["FG"]) #storing the string

			# print (playerstore["threeP"])
			threep = ' '.join(playerstore["threeP"]) #storing the string

			# print (playerstore["FT"])
			ft = ' '.join(playerstore["FT"]) #storing the string

			# print (playerstore["RPG"])
			rpg = ' '.join(playerstore["RPG"]) #storing the string

			# print (playerstore["APG"])
			apg = ' '.join(playerstore["APG"]) #storing the string

			# print (playerstore["SPG"])
			spg = ' '.join(playerstore["SPG"]) #storing the string

			# print (playerstore["BPG"])
			bpg = ' '.join(playerstore["BPG"]) #storing the string

			# print (playerstore["PPG"])
			ppg = ' '.join(playerstore["PPG"]) #storing the string
			   #passing the string that will be indexed
			name = ' '.join(playerstore["Name"])
			writer.add_document(Year= year, Team=team, GP=gp, GS=gs, MPG=mpg, FG=fg,
			threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg, Name=name)
			
	writer.commit()
			
def main():
    #indexing()
	ix = createIndex()
	method_1(ix)

	queryIndex("Name", "Alvan Adams", ix)

	
if __name__ == '__main__':
    main()