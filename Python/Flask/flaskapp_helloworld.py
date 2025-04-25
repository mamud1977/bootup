from flask import Flask, redirect, url_for, request


# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

from flask import Flask 

app = Flask(__name__) 

# Pass the required route to the decorator. 

@app.route('/user/<int:id>') 
def show_id(id): 
    # Shows the post with given id. 
    return f'you entered the id : {id}'


@app.route('/user/<username>') 
def show_user(username): 
    # Greet the user 
    return f'Hello {username} !'

@app.route("/") 
def index(): 
	return "Homepage"

@app.route("/hello") 
def hello(): 
	return "Hello page"
	


# main driver function
if __name__ == '__main__':



    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)