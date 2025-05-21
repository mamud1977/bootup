from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        print("type:", type(username))
        print(f"test: {username}")   
        return "Input successfully captured..."

    return render_template("test_login.html")

if __name__ == "__main__":
    app.run(debug =True)