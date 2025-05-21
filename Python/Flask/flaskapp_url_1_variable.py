from flask import Flask


app = Flask(__name__)

@app.route('/')
def msg():
    return "Welcome"

# We defined string  function
@app.route('/v/<var>')
def vstring(var):
    return f"you passed string: {var}"

@app.route('/v/<int:var>')
def vint(var):
    return f"you passed integer: {var}"

# define float function
@app.route('/v/<float:var>')
def vfloat(var):
    return f"you passed float: {var}"

# we run app debugging mode
app.run(debug=True)