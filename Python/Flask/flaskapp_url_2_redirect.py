# import flast module
from flask import Flask, redirect, url_for, redirect, render_template, request

# instance of flask application
app = Flask(__name__)

# home route that redirects to 
# helloworld page
@app.route("/")
def root():
	return redirect("/home")

# route that returns hello world text
@app.route("/home")
def home():
	return "<p>We are at the home page</p>"

# decorator for route(argument) function
@app.route('/admin')
# binding to hello_admin call
def hello_admin():
    return 'Hello Admin'

@app.route('/<guest>')
# binding to hello_admin call
def hello_guest(guest):
    return f'Hello {guest}'

@app.route('/user/<name>')
def hello_user(name):
 
    # dynamic binding of URL to function
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))





if __name__ == '__main__':
	app.run(debug=True)
