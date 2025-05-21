from fileinput import filename 
from flask import *
app = Flask(__name__) 

@app.route('/fileupload') 
def fileupload(): 
	return render_template("fileupload.html") 

@app.route('/success', methods = ['POST']) 
def success(): 
	if request.method == 'POST': 
		f = request.files['file'] 
		f.save(f.filename) 
		return render_template("fileupload_success.html", name = f.filename) 

if __name__ == '__main__': 
	app.run(debug=True)
