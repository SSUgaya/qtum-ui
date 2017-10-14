from flask import Flask, render_template
import json
import os
app = Flask(__name__)

def get_info():
    p = os.popen("/home/pi/qtum-wallet/bin/qtum-cli getinfo").read()
    parsed_json = json.loads(p)
    return parsed_json

def get_stake():
    p = os.popen("/home/pi/qtum-wallet/bin/qtum-cli getstakinginfo").read()
    parsed_json = json.loads(p)
    return parsed_json

@app.route('/')
def index():
    return render_template('index.html', info_output=get_info(), stake_output=get_stake())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
