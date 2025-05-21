from flask import Flask, render_template, request, send_file, redirect
from jinja2 import Template
from io import BytesIO

app = Flask(__name__)


@app.route("/")
def root():
    return render_template("main.html")


@app.route("/home")
def home():
    return render_template("main.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form.get('username')
        #username = request.form['username']
        print(f'user name: {username}')
        print("type:", type(username))
        return "Input successfully captured..."
    
    return render_template("signup.html")




@app.route("/success")
def success():
    return render_template("success.html")

### POC SCRIPTS .....................

@app.route("/jinja2_parameter_pass")
def jinja2_parameter_pass():
    # variables that contain placeholder data 
    name = 'Abrar'
    email = 'praiseabrar@gmail.com'
    family = ["Mamud", "Afruja","Ishrat","Zeenat"] 
    sites = ['twitter', 'facebook', 'instagram', 'whatsapp']
    return render_template("jinja2_parameter_pass.html", sites=sites)

@app.route("/jinja2")
def jinja2():
    return render_template("jinja2.html")

@app.route("/jscript")
def jscript():
    return render_template("test-javascript.html")




if __name__ == "__main__":
    app.run(debug =True)


