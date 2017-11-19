from flask import Flask, render_template, request, flash, url_for, redirect, send_file
from flask_qrcode import QRcode
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, PasswordField
from wtforms.validators import InputRequired, DataRequired, NumberRange
import time
import json
import os
import subprocess


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD']=True
QRcode(app)

class SendForm(FlaskForm):
    address = StringField('address', validators=[InputRequired(message='Address cannot be blank')])
    amount = StringField('amount', validators=[InputRequired(message='Invalid amount')])
    description = StringField('description')
    to_label = StringField('to_label')
    passwd = PasswordField('password', validators=[DataRequired(message='Passphrase cannot be blank')])

class NewAddressForm(FlaskForm):
    account_address = StringField('account_address')
    account_name = StringField('account_name')
    requested_amount = StringField('requested_amount')
    message = StringField('message')

class QtumPassword(FlaskForm):
    passphrase = PasswordField('passphrase', validators=[DataRequired(message='Passphrase cannot be blank')])

def qtum_info(x='getwalletinfo', y=''):
    process = subprocess.Popen("~/qtum-wallet/bin/qtum-cli %s %s" % (x, y), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = process.communicate()
    if process.returncode != 0:
        return None
    result = str(out,'utf-8')
    parsed_result = json.loads(result)
    return parsed_result

def get_wallet_version():
    version = os.popen("/users/Boss/qtum-wallet/bin/qtum-cli --version").read()
    current_version = {'version' : version}
    current_version = {'version': version.rstrip() for key, value in current_version.items()}
    return current_version

def get_time():
    p = os.popen("/users/Boss/qtum-wallet/bin/qtum-cli getstakinginfo | grep expectedtime | cut -d':' -f2").read()
    time = int(p) / 60 / 60 / 24
    expected_stake = round(time)
    return expected_stake

def last_sent_tx():
    last_tx = qtum_info("listtransactions '*'", 100)
    all_sent = {}
    for send in last_tx:
        if send['category'] == "send" or  send['category'] == "move":
            all_sent.update(send)
    return all_sent

def get_address():
    get_address = os.popen('/users/Boss/qtum-wallet/bin/qtum-cli getaccountaddress ""').read()
    return get_address

def get_account_addresses():
    list_accounts = os.popen('/users/Boss/qtum-wallet/bin/qtum-cli listaccounts').read()
    accounts = json.loads(list_accounts)
    all_addresses = {}
    for x in accounts:
        p = os.popen('/users/Boss/qtum-wallet/bin/qtum-cli getaddressesbyaccount "%s"' % x).read()
        parsed_json = json.loads(p)
        all_addresses[x] = parsed_json
    return all_addresses

def donate_piui():
    donation_string = 'qtum:QceE7a47byDhFs9wy2c2ZdXz4yfT4RZLJQ?amount=&label=Donation&message=PIUI-Donation'
    return donation_string

def qrcode_format(address, amount, name, msg):
    response = 'qtum:%s?amount=%s&label=%s&message=%s' % (address, amount, name, msg)
    return response

@app.route('/')
def index():
    if qtum_info() == None:
        return redirect(url_for('offline'))
    date = time
    return render_template('index.html', qtum_wallet=qtum_info(), get_current_block=qtum_info("getinfo"), list_tx=qtum_info("listtransactions '*'", 100), wallet_version=get_wallet_version(), stake_output=qtum_info("getstakinginfo"), stake_time=get_time(), **locals())

@app.route('/send', methods=['GET', 'POST'])
def send():
    date = time
    form = SendForm()
    max_spend = qtum_info()
    if form.validate_on_submit():
        spendable = float(max_spend['balance'])
        amount = form.amount.data
        input_amount = float(amount)
        address = form.address.data
        passwd = form.passwd.data
        description = form.description.data
        to_label = form.to_label.data
        passwd_time = '20'
        if input_amount > spendable:
            flash('Opps! You Entered an Invalid Amount.', 'error')
            return redirect(url_for('send'))
        unlock = ['/users/Boss/qtum-wallet/bin/qtum-cli', 'walletpassphrase']
        unlock.append(passwd)
        unlock.append(passwd_time)
        process = subprocess.Popen(unlock, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = process.communicate()[1:2]
        if process.returncode != 0:
            flash('Opps! Wallet Passphrase is Incorrect.', 'error')
            return redirect(url_for('send'))
        command = ['/users/Boss/qtum-wallet/bin/qtum-cli', 'sendtoaddress']
        command.append(address)
        command.append(amount)
        command.append(description)
        command.append(to_label)
        process = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (out,err) = process.communicate()
        if process.returncode != 0:
            flash('Opps! You Entered an Invalid Address.', 'error')
            return redirect(url_for('send'))
        result = str(out,'utf-8')
        flash("Success! TX ID: %s" % result, 'msg')
        return redirect(url_for('send'))
    return render_template('send.html', last_tx=qtum_info("listtransactions '*'", 100), get_unspent=qtum_info('listunspent', 0), qtum_wallet=qtum_info(), **locals())

@app.route('/receive')
def receive():
    date = time
    form = NewAddressForm()
    return render_template('receive.html', form=form, date=time, get_received=qtum_info("listtransactions '*'", 100), get_address=get_address(), account_add=get_account_addresses(), qtum_wallet=qtum_info())

@app.route('/new_address', methods=['POST'])
def new_address():
    date = time
    form = NewAddressForm()
    if form.validate_on_submit():
        account_address = form.account_address.data
        account_name = form.account_name.data
        requested_amount = form.requested_amount.data
        message = form.message.data
        if account_address == '':
            command = ['/users/Boss/qtum-wallet/bin/qtum-cli', 'getnewaddress']
            command.append(account_name)
            process = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            (out,err) = process.communicate()
            if process.returncode != 0:
                flash('Opps! Something went wrong, try again.', 'error')
                return redirect(url_for('receive'))
            result = str(out,'utf-8')
            flash(result, 'msg')
            return render_template('receive.html', form=form, date=time, get_received=qtum_info("listtransactions '*'", 100), qrcode_reposnse=qrcode_format(result, requested_amount, account_name, message), get_address=get_address(), account_add=get_account_addresses(), qtum_wallet=qtum_info())
    flash(account_address, 'msg')
    return render_template('receive.html', form=form, date=time, get_received=qtum_info("listtransactions '*'", 100), qrcode_reposnse=qrcode_format(account_address, requested_amount, account_name, message), get_address=get_address(), account_add=get_account_addresses(), qtum_wallet=qtum_info())

@app.route('/transaction')
def transaction():
    date = time
    return render_template('transactions.html', date=time, all_tx=qtum_info("listtransactions '*'", 100))

@app.route('/setup')
def setup():
    form = QtumPassword()
    return render_template('settings.html', form=form, qtum_wallet=qtum_info("getinfo"), donate_piui=donate_piui())

@app.route('/encrypt_wallet', methods=['POST'])
def encrypt_wallet():
    form = QtumPassword()
    if form.validate_on_submit():
        passphrase = form.passphrase.data
        command = ['/users/Boss/qtum-wallet/bin/qtum-cli', 'encryptwallet']
        command.append(passphrase)
        process = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (out,err) = process.communicate()
        if process.returncode != 0:
            flash('Opps! Something went wrong.', 'error1')
            return redirect(url_for('setup'))
        result = str(out,'utf-8')
        flash(result, 'msg')
        restart_qtum = ['/users/Boss/qtum-wallet/bin/qtumd', '-daemon']
        time.sleep(2)
        subprocess.run(restart_qtum)
        time.sleep(5)
        return redirect(url_for('index'))
    return render_template('settings.html', form=form, qtum_wallet=qtum_info("getinfo"), donate_piui=donate_piui())

@app.route('/staking_service', methods=['POST'])
def staking_service():
    form = QtumPassword()
    if form.validate_on_submit():
        passphrase = form.passphrase.data
        staking_enable = '~/qtum-wallet/bin/qtum-cli walletpassphrase "%s" 9999999999 true' % passphrase
        process = subprocess.Popen(staking_enable, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        (out,err) = process.communicate()
        if process.returncode != 0:
            flash('Opps! Wallet Passphrase is Incorrect.', 'error')
            return redirect(url_for('setup'))
        flash('Success! Wallet is now Staking.', 'msg')
        return redirect(url_for('setup'))
    return render_template('settings.html', form=form, qtum_wallet=qtum_info("getinfo"), donate_piui=donate_piui())

@app.route('/lock_wallet')
def lock_wallet():
    process = subprocess.run("~/qtum-wallet/bin/qtum-cli walletlock", shell=True)
    flash('Success! Wallet is Locked', 'msg')
    return redirect(url_for('setup'))

@app.route('/offline')
def offline():
    return render_template('offline.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
