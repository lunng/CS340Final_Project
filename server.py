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
	return render_template('Search.html')
	
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


	
def main():
	app.run(debug=True)

if __name__ == '__main__':
	main()
