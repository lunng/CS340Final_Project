from flask import Flask, render_template, url_for, request
from jinja2 import TemplateNotFound
import whoosh_script
import whoosh
from whoosh.index import create_in
from whoosh.fields import*
from whoosh.qparser import QueryParser
import re
import json
import os

app = Flask(__name__)
cache_query = None
playerDetail_cache = None

@app.route('/', methods=['GET', 'POST'])
def index():
	# print("Someone is at page %s" % pagename)
	# try:
		# return render_template(pagename)
	# except TemplateNotFound:
		# return render_template('404.html')
	return render_template('Search.html')

def searchButton(data):
	global playerDetail_cache
	playerDetail = data.getlist('playerDetail')
	if 'playerDetail' in data:
		playerDetail = data.getlist('playerDetail')
		playerDetail_cache = data.getlist('playerDetail')
	else:
		playerDetail = playerDetail_cache
		
	return playerDetail
	#create for loop to loop through the list, then ask conditions like if playerDetail == element in array: do something

@app.route('/my-link/')
def my_link():
	print('I got clicked!')
	return 'Click.'

@app.route('/homepage.html',  methods=['GET', 'POST'])
def homepage():
	print("Accessed homepage")
	return render_template('homepage.html')

@app.route('/Search.html',  methods=['GET', 'POST'])
def search():
	print("Accessed searchpage")
	if request.method == "POST":
		return request.form.get('Name')
	return render_template('Search.html')

@app.route('/aboutUs.html',  methods=['GET', 'POST'])
def about():
	print("Accessed searchpage")
	return render_template('aboutUs.html')

@app.route('/results/', methods=['GET', 'POST'])
def results():
	if request.method == 'POST':
		#original variable name is data
		data2 = request.form
	else:
		#original variable name is data
		data2 = request.args

	query = data2.get('searchterm')
	global cache_query
	if 'searchterm' in data2:
		query = data2.get('searchterm')
		cache_query = data2.get('searchterm')
	else:
		query = cache_query

	if 'page_number' in data2:
		query2 = data2.get('page_number')
	else:
		query2 = 1

	print("You searched for: " + query)

	nstr = re.sub(r'[?|$|.|!|#|@|~]',r'',query)
	nestr = re.sub(r'[^a-zA-Z0-9 ]',r'',nstr)
	print("clean query : " + nestr)
	print("clean query : " + nstr)
	ix = whoosh_script.openIndex()

	searchType = searchButton(data2)
	print("Search type")
	print(searchType)
	data = {}

	data,page_data, page_count = whoosh_script.queryIndex(searchType, query, ix, query2)
	page_count = list(range(1,page_count+1))


	return render_template('results.html', results=zip(page_data["filenames"], page_data["playernames"]) , page_count = page_count) #,results=zip(firstName, lastName))

@app.route('/', methods=['GET', 'POST'])
def player_values(JSON_path, graph_paths):
		#for loop for the array of returned results
		# for file in json_files:
		# 	with open("./Players JSONS/" + file, 'r') as f:
		with open(JSON_path, 'r') as f:
			player_page = json.load(f)
			for title in player_page:
				if title == "Year" or title == "Team" or title == "Name":
					continue
				pathname = "chartsdir/"
				try:
					pathname += player_page["Name"][0]
					pathname += title
					pathname += ".png"
				except:
					continue
				graph_paths.append(pathname)
			#getting the values from the json pages
			year = player_page["Year"]#storing the string
			team = player_page["Team"] #storing the list of stats
			gp = player_page["GP"] #storing the list of stats
			gs = player_page["GS"] #storing the list of stats
			mpg = player_page["MPG"] #storing the list of stats
			fg = player_page["FG"] #storing the list of stats
			threep = player_page["threeP"] #storing the list of stats
			ft = player_page["FT"] #storing the list of stats
			rpg = player_page["RPG"] ##storing the list of stats
			apg = player_page["APG"]#storing the list of stats
			spg = player_page["SPG"] #storing the list of stats
			bpg = player_page["BPG"] #storing the list of stats
			ppg = player_page["PPG"] #storing the list of stats
			name = player_page["Name"][0] #storing the list of stats
		return year, team, gp, gs, mpg, fg, threep, ft, rpg, apg, spg, bpg, ppg, name
#individual player page

@app.route('/player_pages/', methods=['GET', 'POST'])
def player_pages():
	if request.method == 'POST':
		#original variable name is data
		data = request.form
	else:
		#original variable name is data
		data = request.args

	JSON_path = data.get('Name')
	graph_paths = []
	Year, Team, GP, GS, MPG, FG, threeP, FT, RPG, APG, SPG, BPG, PPG, Name = player_values(JSON_path, graph_paths)
	print(graph_paths)
	return render_template('player_pages.html', results=zip(Year, Team, GP, GS, MPG, FG, threeP, FT, RPG, APG, SPG, BPG, PPG), name=Name, paths=graph_paths)

def main():
	app.run(debug=True)

if __name__ == '__main__':
	main()
