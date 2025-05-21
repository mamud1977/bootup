from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return 'Hello World'

@app.route('/hello')
def signup():
   #return 'signup page will be launched'
   return render_template('flaskapp_1_helloworld.html')

@app.route('/hello/<name>')
def hello_name(name):
   return f'Hello {name}!'

@app.route('/login')
def signup():
   #return 'signup page will be launched'
   return render_template('flaskapp_1_helloworld_login.html')

if __name__ == '__main__':

    app.run(debug=True)