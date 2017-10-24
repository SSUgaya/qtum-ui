from flask import Flask, render_template, request
from flask_wtf import Form
from wtforms import StringField, DecimalField, BooleanField, PasswordField
import json
import os
import subprocess


app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySeuperSecretKeyHere'

class SendForm(Form):
    address = StringField('qtumAddress')
    amount = DecimalField('qtumAmount')
    label = StringField('qtumLabel')
    description = StringField('qtumDescription')
    passwd = PasswordField('qtumPass')
    feeAmount = BooleanField('qtumFee')

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

@app.route('/send', methods=['GET', 'POST'])
def send():
    form = SendForm()
    return render_template('send.html', form=form, info_output=get_info(), stake_output=get_stake(), stake_time=get_time())

@app.route('/receive')
def receive():
    return render_template('receive.html', info_output=get_info(), stake_output=get_stake(), stake_time=get_time())

@app.route('/transaction')
def transaction():
    return render_template('transactions.html', info_output=get_info(), stake_output=get_stake(), stake_time=get_time())

@app.route('/contract')
def contract():
    return render_template('contract.html', info_output=get_info(), stake_output=get_stake(), stake_time=get_time())

@app.route('/send_qtum', methods=['POST'])
def send_qtum():
    address = request.form['qtumAddress']
    amount = request.form['qtumAmount']
    passwd = request.form['qtumPass']
    label = request.form['qtumLabel']
    description = request.form['qtumDescription']
    passwd_time = '20'
    unlock = ['/home/pi/qtum-wallet/bin/qtum-cli', 'walletpassphrase']
    unlock.append(passwd)
    unlock.append(passwd_time)
    subprocess.run(unlock)
    command = ['/home/pi/qtum-wallet/bin/qtum-cli', 'sendtoaddress']
    command.append(address)
    command.append(amount)
    command.append(label)
    command.append(description)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    (out,err) = process.communicate()
    return out

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
