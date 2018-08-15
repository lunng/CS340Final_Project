from flask import Flask, render_template, url_for, request
from jinja2 import TemplateNotFound
import whoosh_script
import whoosh
from whoosh.index import create_in
from whoosh.fields import*
from whoosh.qparser import QueryParser

import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	# print("Someone is at page %s" % pagename)
	# try:
		# return render_template(pagename)
	# except TemplateNotFound:
		# return render_template('404.html')
	return render_template('Search.html')

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

#checkbox
# @app.route('/', methods=['GET', 'POST'])
# def checkbox():
# 	# if request.method == "POST":
# 	# 	return request.form.get('Name')
#
# 	 if request.form.getlist('Name'):
# 	 	print ("something!")
# 	check = False
#
#
# 	if request.form.get('Year'):
# 		check = True
# 		print("name check box was checked")
# 		print (check)


@app.route('/aboutUs.html',  methods=['GET', 'POST'])
def about():
	print("Accessed searchpage")
	return render_template('aboutUs.html')

@app.route('/results/', methods=['GET', 'POST'])
def results():
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	query = data.get('searchterm')
	print("You searched for: " + query)
	ix = whoosh_script.openIndex()
	data = whoosh_script.queryIndex("Name", query, ix)


	# firstName = ['Ben','Sarah', 'Xandar', 'Ellewyn']
	# lastName = ['McCamish', 'G', 'Quazar', 'Sabbeth']
	return render_template('results.html', query=data) #,results=zip(firstName, lastName))

@app.route('/', methods=['GET', 'POST'])
def player_values():
		#for loop for the array of returned results
		# for file in json_files:
		# 	with open("./Players JSONS/" + file, 'r') as f:
		with open("./Players JSONS/Austin_Carr.json", 'r') as f:
			player_page = json.load(f)
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
@app.route('/player_pages', methods=['GET', 'POST'])
def player_pages():
		#removed passing name
		 Year, Team, GP, GS, MPG, FG, threeP, FT, RPG, APG, SPG, BPG, PPG, Name = player_values()
		 return render_template('player_pages.html', results=zip(Year, Team, GP, GS, MPG, FG, threeP, FT, RPG, APG, SPG, BPG, PPG), name=Name)
def main():
	app.run(debug=True)

if __name__ == '__main__':
	main()
