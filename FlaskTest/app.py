from flask import Flask, render_template,jsonify
from random import sample
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('charts.html')

@app.route('/data')
def data():
    return jsonify({'results':sample(range(1,20),10)})

if __name__ == '__main__':
    app.run(port=9999)
