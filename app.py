from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/cakes')
def cakes():
    return 'Yummy Cakes!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
