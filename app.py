from flask import Flask, url_for
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')
    
@app.route("/configure")
def configure():
    return render_template('configure.html')

if __name__=="__main__":
	app.run(debug=True)
