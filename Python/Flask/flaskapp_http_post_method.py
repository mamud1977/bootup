from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/square', methods=['GET', 'POST'])
def squarenumber():
    if request.method == 'POST':
        num = request.form.get('num')     
        is_empty = lambda x: not x

        if num is None: # No number entered, show input form
            return render_template('squarenum_post.html')
        
        elif is_empty(num):
            return render_template('squarenum_post.html')
        
        else:
            square = int(num) ** 2
            return render_template('answer.html', squareofnum=square, num=num)
    return render_template('squarenum_post.html')

if __name__ == '__main__':
    app.run(debug=True)
