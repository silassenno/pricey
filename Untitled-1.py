from flask import Flask
from flask import render_template
from sqlite3 import connect
from flask import request

app = Flask("pricey")
app.connection=connect("pricey.db")
@app.route("/expense/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        cursor=app.connection.cursor()
        cursor.execute("INSERT INTO expense")
        #insert into database
        pass
    return render_template('addexpense.html')
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)