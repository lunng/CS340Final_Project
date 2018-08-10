#whoosh http://whoosh.readthedocs.io/en/latest/quickstart.html
import whoosh
from whoosh.index import create_in
from whoosh.fields import*
from whoosh.qparser import QueryParser
import json
import os
def indexing(year, team, gp, gs, mpg, fg, threep, ft, rpg, apg, spg, bpg, ppg):
    #what we're searching over
    schema = Schema(Year=TEXT(stored=True), Team=TEXT(stored=True), GP=TEXT(stored=True),
    GS=TEXT(stored=True), MPG=TEXT(stored=True), FG=TEXT(stored=True), threeP=TEXT(stored=True),
    FT=TEXT(stored=True), RPG=TEXT(stored=True),APG=TEXT(stored=True),SPG=TEXT(stored=True),
    BPG=TEXT(stored=True), PPG=TEXT(stored=True),)

    #creates a Storage object to contain the index
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)

    #ix = open_dir("index")
    #writer() lets you add documents to the index.
    writer = ix.writer()

    writer.add_document(Year= year, Team=team, GP=gp, GS=gs, MPG=mpg, FG=fg,
    threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg)

    # writer.add_document(Year= year, Team=team, GP=gp, GS=gs, MPG=mpg, FG=fg,
    # threeP=threep, FT=ft, RPG=rpg, APG=apg, SPG=spg, BPG=bpg, PPG=ppg)

    writer.commit()

     #searching test
    with ix.searcher() as searcher:
         query = QueryParser("Year", ix.schema).parse("1969-70")
         results = searcher.search(query)
         results[0]
         print("____________________________________________________________________")
         print("results:" + str(results[0]))

    # {"title": u"First document", "path": u"/a"}

def method_1():
    json_files = os.listdir("./Players JSONS")
    #to do for loop for all players the json files need to n
    # for file in json_files:
    #     with open("./Players JSONS/" + file, 'r') as f:
    with open("./Players JSONS/Kareem_Abdul-Jabbar.json", 'r') as f:
        playerstore = json.load(f)

        ' '.join(playerstore["Year"])   #changes commas to spaces
        year = ' '.join(playerstore["Year"]) #storing the string

        print (playerstore["Team"])
        ' '.join(playerstore["Team"])   #changes commas to spaces
        team = ' '.join(playerstore["Team"]) #storing the string

        print (playerstore["GP"])
        ' '.join(playerstore["GP"])   #changes commas to spaces
        gp = ' '.join(playerstore["GP"]) #storing the string

        print (playerstore["GS"])
        ' '.join(playerstore["GS"])   #changes commas to spaces
        gs = ' '.join(playerstore["GS"]) #storing the string

        print (playerstore["MPG"])
        ' '.join(playerstore["MPG"])   #changes commas to spaces
        mpg = ' '.join(playerstore["MPG"]) #storing the string

        print (playerstore["FG"])
        ' '.join(playerstore["FG"])   #changes commas to spaces
        fg = ' '.join(playerstore["FG"]) #storing the string

        print (playerstore["threeP"])
        ' '.join(playerstore["threeP"])   #changes commas to spaces
        threep = ' '.join(playerstore["threeP"]) #storing the string

        print (playerstore["FT"])
        ' '.join(playerstore["FT"])   #changes commas to spaces
        ft = ' '.join(playerstore["FT"]) #storing the string

        print (playerstore["RPG"])
        ' '.join(playerstore["RPG"])   #changes commas to spaces
        rpg = ' '.join(playerstore["RPG"]) #storing the string

        print (playerstore["APG"])
        ' '.join(playerstore["APG"])   #changes commas to spaces
        apg = ' '.join(playerstore["APG"]) #storing the string

        print (playerstore["SPG"])
        ' '.join(playerstore["SPG"])   #changes commas to spaces
        spg = ' '.join(playerstore["SPG"]) #storing the string

        print (playerstore["BPG"])
        ' '.join(playerstore["BPG"])   #changes commas to spaces
        bpg = ' '.join(playerstore["BPG"]) #storing the string

        print (playerstore["PPG"])
        ' '.join(playerstore["PPG"])   #changes commas to spaces
        ppg = ' '.join(playerstore["PPG"]) #storing the string
           #passing the string that will be indexed
        indexing(year, team, gp, gs, mpg, fg, threep, ft, rpg, apg, spg, bpg, ppg)
def main():
    #indexing()
    method_1()
if __name__ == '__main__':
    main()
