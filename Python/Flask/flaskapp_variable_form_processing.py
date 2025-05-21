from flask import Flask, request, render_template, abort

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        print("type:", type(username))
 
        is_empty = lambda x: not x

        if username is None: # No number entered, show input form
            return render_template('form.html')
        
        elif is_empty(username):
            return render_template('form.html')
        
        else:
            print(f"test: {username}")   
            return "Input successfully captured..."
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, port=8001)
