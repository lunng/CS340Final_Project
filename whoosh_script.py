#whoosh http://whoosh.readthedocs.io/en/latest/quickstart.html
import whoosh
from whoosh.index import create_in
from whoosh.fields import*
from whoosh import qparser
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import MultifieldParser
import json
import os

def createIndex():
#what we're searching over
	schema = Schema(Year=TEXT(stored=True), Team=TEXT(stored=True), GP=TEXT(stored=True),
	GS=TEXT(stored=True), MPG=TEXT(stored=True), FG=TEXT(stored=True), threeP=TEXT(stored=True),
	FT=TEXT(stored=True), RPG=TEXT(stored=True),APG=TEXT(stored=True),SPG=TEXT(stored=True),
	BPG=TEXT(stored=True), PPG=TEXT(stored=True), Name=TEXT(stored=True), Filename=TEXT(stored=True),)

    #creates a Storage object to contain the index
	if not os.path.exists("indexdir"):
		os.mkdir("indexdir")

	ix = create_in("indexdir", schema)
	return ix

def openIndex():
	storage = FileStorage("indexdir")
	ix = storage.open_index()
	return ix

def addToIndex(year, team, gp, gs, mpg, fg, threep, ft, rpg, apg, spg, bpg, ppg, name, ix):

	writer = ix.writer()
	writer.add_document(Year= year, Team=team, GP=gp, GS=gs, MPG=mpg, FG=fg,
	threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg, Name=name)
	writer.commit()

    # writer.add_document(Year= year, Team=team, GP=gp, GS=gs, MPG=mpg, FG=fg,
    # threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg)



def queryIndex(queryTypes, queryValue, ix, page_num=1):
	page_num = int(page_num)
	
	with ix.searcher() as searcher:
		query = MultifieldParser(queryTypes, ix.schema, group=qparser.OrGroup).parse(queryValue)
		results = searcher.search(query, limit=None)
		counted_results = searcher.search_page(query, page_num)	# first time calling page num is 1
		print('tedt:' + str(counted_results[0]) + str(page_num))
		#length of results
		num = len(results)
		num_pages = int(num / 10)	#because default is floating point

		names_list = {}
		names_list["filenames"] = []
		names_list["playernames"] = []
		for result in results:
			names_list["filenames"].append(result["Filename"])
			names_list["playernames"].append(result["Name"])

		counted_names_list = {}
		counted_names_list["filenames"] = []
		counted_names_list["playernames"] = []

		for result in counted_results:
			counted_names_list["filenames"].append(result["Filename"])
			counted_names_list["playernames"].append(result["Name"])

		return names_list, counted_names_list, num_pages

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
		filename = "./Players JSONS/" + file
		with open(filename, 'r') as f:
	# with open("./Players JSONS/Kareem_Abdul-Jabbar.json", 'r') as f:
			playerstore = json.load(f)
			for index in playerstore:
				i = 0
				for value in playerstore[index]:
					if not value:
						playerstore[index][i] = "-"
					i += 1
			if "Year" in playerstore:
				year = ' '.join(playerstore["Year"]) #storing the string
			else:
				continue
			print(playerstore["Name"])
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
			threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg, Name=name, Filename=filename)

	writer.commit()

def main():
    #indexing()
	ix = createIndex()
	method_1(ix)

	queryIndex("Name", "Jabbar", ix)


if __name__ == '__main__':
    main()
