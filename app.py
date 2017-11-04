from flask import Flask, render_template, request, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length
import time
import json
import os
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySeuperSecretKeyHere'

class SendForm(FlaskForm):
    address = StringField('address')
    amount = StringField('amount')
    label = StringField('label')
    description = StringField('description')
    passwd = PasswordField('password')
    feeAmount = BooleanField('fee')

def get_info(): # On Pi working directory is "/home/pi/qtum-wallet/bin/qtum-cli getinfo"
    p = os.popen("/users/Boss/qtum-wallet/bin/qtum-cli getwalletinfo").read()
    parsed_json = json.loads(p)
    return parsed_json

def get_block(): # On Pi working directory is "/home/pi/qtum-wallet/bin/qtum-cli getinfo"
    p = os.popen("/users/Boss/qtum-wallet/bin/qtum-cli getinfo").read()
    parsed_json = json.loads(p)
    return parsed_json

def get_stake():
    p = os.popen("/users/Boss/qtum-wallet/bin/qtum-cli getstakinginfo").read()
    parsed_json = json.loads(p)
    return parsed_json

def get_time():
    p = os.popen("/users/Boss/qtum-wallet/bin/qtum-cli getstakinginfo | grep expectedtime | cut -d':' -f2").read()
    time = int(p) / 60 / 60 / 24
    expected_stake = round(time)
    return expected_stake

def get_last_tx():
    p = os.popen('/users/Boss/qtum-wallet/bin/qtum-cli listtransactions "*"  50').read()
    parsed_json = json.loads(p)
    return parsed_json

def get_addresses():
    p = os.popen('/users/Boss/qtum-wallet/bin/qtum-cli listunspent').read()
    parsed_json = json.loads(p)
    return parsed_json

def get_account_addresses():
    list_accounts = os.popen('/users/Boss/qtum-wallet/bin/qtum-cli listaccounts').read()
    accounts = json.loads(list_accounts)
    all_addresses = {}
    for x in accounts:
        p = os.popen('/users/Boss/qtum-wallet/bin/qtum-cli getaddressesbyaccount "%s"' % x).read()
        parsed_json = json.loads(p)
        all_addresses[x] = parsed_json
    return all_addresses

@app.route('/')
def index():
    date = time
    return render_template('index.html', get_block=get_block(), last_tx=get_last_tx(), info_output=get_info(), stake_output=get_stake(), stake_time=get_time(), **locals())

@app.route('/send', methods=['GET', 'POST'])
def send():
    date = time
    form = SendForm()
    if form.validate_on_submit():
        address = form.address.data
        amount = form.amount.data
        passwd = form.passwd.data
        label = form.label.data
        description = form.description.data
        passwd_time = '20'
        unlock = ['/users/Boss/qtum-wallet/bin/qtum-cli', 'walletpassphrase']
        unlock.append(passwd)
        unlock.append(passwd_time)
        subprocess.run(unlock)
        command = ['/users/Boss/qtum-wallet/bin/qtum-cli', 'sendtoaddress']
        command.append(address)
        command.append(amount)
        command.append(description)
        command.append(label)
        process = subprocess.Popen(command, stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        (out,err) = process.communicate()
        flash(out)
        return redirect(url_for('send'))

    return render_template('send.html', get_block=get_block(), last_tx=get_last_tx(), info_output=get_info(), stake_output=get_stake(), stake_time=get_time(), **locals())

@app.route('/receive')
def receive():
    form = SendForm()
    return render_template('receive.html', account_add=get_account_addresses(), get_addresses=get_addresses(), get_block=get_block(), info_output=get_info(), stake_output=get_stake(), stake_time=get_time(), **locals())

@app.route('/transaction')
def transaction():
    date = time
    return render_template('transactions.html', get_block=get_block(), last_tx=get_last_tx(), info_output=get_info(), stake_output=get_stake(), stake_time=get_time(), **locals())

@app.route('/contract')
def contract():
    return render_template('contract.html', get_block=get_block(), info_output=get_info(), stake_output=get_stake(), stake_time=get_time())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
