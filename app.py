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

def get_time():
    p = os.popen("/home/pi/qtum-wallet/bin/qtum-cli getstakinginfo | grep expectedtime | cut -d':' -f2").read()
    time = int(p) / 60 / 60 / 24
    expected_stake = round(time)
    return expected_stake

@app.route('/')
def index():
    return render_template('index.html', info_output=get_info(), stake_output=get_stake(), stake_time=get_time())

@app.route('/send')
def send():
    return render_template('send.html', info_output=get_info(), stake_output=get_stake(), stake_time=get_time())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
