from flask import Flask
from flask import render_template
from sqlite3 import connect

app = Flask("pricey")
app.connect=connect("pricey.db")
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)