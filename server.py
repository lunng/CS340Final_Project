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

	#checkbox
	# @app.route('/', methods=['GET', 'POST'])
	# if request.method == "POST":
	# return request.form.get('Name')

	#def checkbox():
	#	if request.form.getlist('Name'):
	#		print ("something!")
	#		check = False

			#about the playerDetail checkboxes
def searchButton(data):
	playerDetail = data.getlist('playerDetail')
	print (playerDetail)
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
	print("You searched for: " + query)
	ix = whoosh_script.openIndex()
	data = whoosh_script.queryIndex("Name", query, ix)
	# firstName = ['Ben','Sarah', 'Xandar', 'Ellewyn']
	# lastName = ['McCamish', 'G', 'Quazar', 'Sabbeth']
	#this search button gives us the correct returns for list
	searchButton(data2)
	return render_template('results.html', query=data) #,results=zip(firstName, lastName))

	



def main():
	app.run(debug=True)

if __name__ == '__main__':
	main()
