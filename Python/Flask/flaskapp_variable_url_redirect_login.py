# importing redirect 
from flask import Flask, redirect, url_for, render_template, request 

# Initialize the flask application 
app = Flask(__name__) 

# It will load the form template which 
# is in login.html 
@app.route('/') 
def index(): 
	return render_template("login.html") 


@app.route('/success') 
def success(): 
	return "logged in successfully"

# loggnig to the form with method POST or GET 
@app.route("/login") 
def login(): 
	# if the method is POST and Username is admin then 
	# it will redirects to success url. 
    return "logged in successfully"



if __name__ == '__main__': 
	app.run(debug=True) 
