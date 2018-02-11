from flask import Flask, render_template, request, flash, url_for, redirect, send_file
from flask_qrcode import QRcode
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, NumberRange
from flask_bootstrap import Bootstrap
import time
import json
import os
import subprocess


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD']=True
QRcode(app)
Bootstrap(app)

class SendForm(FlaskForm):
    address = StringField('address', validators=[InputRequired(message='Address cannot be blank')])
    amount = StringField('amount', validators=[InputRequired(message='Invalid amount')])
    description = StringField('description')
    to_label = StringField('to_label')
    passwd = PasswordField('password', validators=[DataRequired(message='Passphrase cannot be blank')])
    include_fee = BooleanField('include_fee', default=False)

class NewAddressForm(FlaskForm):
    account_address = StringField('account_address')
    account_name = StringField('account_name')
    requested_amount = StringField('requested_amount')
    message = StringField('message')

class QtumPassword(FlaskForm):
    passphrase = PasswordField('passphrase', validators=[DataRequired(message='Passphrase cannot be blank')])

class AddNode(FlaskForm):
    nodeaddress = StringField('nodeaddress', validators=[DataRequired(message='Please enter a vaild IP Address')])

def qtum_info(x='getwalletinfo', y=''):
    process = subprocess.Popen("~/qtum-wallet/bin/qtum-cli %s %s" % (x, y), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = process.communicate()
    if process.returncode != 0:
        return None
    result = str(out,'utf-8')
    parsed_result = json.loads(result)
    return parsed_result

def qtum(x):
    process = subprocess.Popen("~/qtum-wallet/bin/qtum-cli %s" % x, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = process.communicate()
    if process.returncode != 0:
        return None
    result = str(out,'utf-8')
    return result

def wallet_start_up():
    start_wallet = '~/qtum-wallet/bin/qtumd -daemon=1'
    process = subprocess.Popen(start_wallet, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    (out,err) = process.communicate()
    if process.returncode != 0:
        return None
    return out

def qtum_unlock(passwd, duration, stake='false'):
    wallet_unlock = '~/qtum-wallet/bin/qtum-cli walletpassphrase "%s" %d %s' % (passwd, duration, stake)
    process = subprocess.Popen(wallet_unlock, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    (out,err) = process.communicate()
    if process.returncode != 0:
        return None
    return out

def get_time():
    time_to_stake = qtum("getstakinginfo | grep expectedtime | cut -d':' -f2")
    time = int(time_to_stake) / 60 / 60 / 24
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
    response = qtum("getaccountaddress ''")
    return response

def get_account_addresses():
    list_accounts = qtum_info("listaccounts")
    all_addresses = {}
    for x in list_accounts:
        each_address = qtum("getaddressesbyaccount '%s'" % x)
        parsed_json = json.loads(each_address)
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
    return render_template('index.html',date=date, qtum_mempool=qtum_info("getmempoolinfo"), qtum_network=qtum_info("getnettotals"), qtum_wallet=qtum_info(), get_current_block=qtum_info("getinfo"), list_tx=qtum_info("listtransactions '*'", 100), wallet_version=qtum("--version"), stake_output=qtum_info("getstakinginfo", ""), stake_time=get_time())

@app.route('/send', defaults={'selected_address' : ''})
@app.route('/send/<selected_address>', methods=['GET', 'POST'])
def send(selected_address):
    date = time
    form = SendForm()
    return render_template('send.html', address=selected_address, date=date, form=form, last_tx=qtum_info("listtransactions '*'", 100), get_unspent=qtum_info('listunspent', 0), qtum_wallet=qtum_info())

@app.route('/send_qtum', methods=['POST'])
def send_qtum():
    date = time
    form = SendForm()
    max_spend = qtum_info()
    fee = str(form.include_fee.data)
    if form.validate_on_submit():
        spendable = float(max_spend['balance'])
        amount = float(form.amount.data)
        if amount > spendable:
            flash('Opps! You Entered an Invalid Amount.', 'error')
            return redirect(url_for('send'))
        start_unlock = qtum_unlock(form.passwd.data, 20)
        if start_unlock == None:
            flash('Opps! Wallet Passphrase is Incorrect.', 'error')
            return redirect(url_for('send'))
        send_qtum = qtum("sendtoaddress '%s' %f '%s' '%s' %s" % (form.address.data, amount, form.description.data, form.to_label.data, fee.lower()))
        if send_qtum == None:
            flash('Opps! You Entered an Invalid Address.', 'error')
            return redirect(url_for('send'))
        flash("Success! TX ID: %s" % send_qtum, 'msg')
        return redirect(url_for('send'))
    return render_template('send.html', date=date, form=form, last_tx=qtum_info("listtransactions '*' 100"), get_unspent=qtum_info('listunspent', 0), qtum_wallet=qtum_info())

@app.route('/receive', defaults={'selected_address' : ''})
@app.route('/receive/<selected_address>')
def receive(selected_address):
    date = time
    form = NewAddressForm()
    return render_template('receive.html', address=selected_address, form=form, date=time, get_received=qtum_info("listtransactions '*' 100"), get_address=get_address(), account_add=get_account_addresses(), qtum_wallet=qtum_info())

@app.route('/new_address', methods=['POST'])
def new_address():
    date = time
    form = NewAddressForm()
    if form.validate_on_submit():
        if form.account_address.data == '':
            get_new_address = qtum("getnewaddress '%s'" % form.account_name.data)
            if get_new_address == None:
                flash('Opps! Something went wrong, try again.', 'error')
                return redirect(url_for('receive'))
            flash(get_new_address, 'msg')
            return render_template('receive.html', form=form, date=time, get_received=qtum_info("listtransactions '*'", 100), qrcode_reposnse=qrcode_format(get_new_address, form.requested_amount.data, form.account_name.data, form.message.data), get_address=get_address(), account_add=get_account_addresses(), qtum_wallet=qtum_info())
    flash(form.account_address.data, 'msg')
    return render_template('receive.html', form=form, date=time, get_received=qtum_info("listtransactions '*'", 100), qrcode_reposnse=qrcode_format(form.account_address.data, form.requested_amount.data, form.account_name.data, form.message.data), get_address=get_address(), account_add=get_account_addresses(), qtum_wallet=qtum_info())

@app.route('/transaction')
def transaction():
    date = time
    return render_template('transactions.html', date=time, all_tx=qtum_info("listtransactions '*'", 100))

@app.route('/setup')
def setup():
    form = QtumPassword()
    form_addnode = AddNode()
    return render_template('settings.html', form=form, form_addnode=form_addnode, qtum_wallet=qtum_info("getinfo"), donate_piui=donate_piui())

@app.route('/encrypt_wallet', methods=['POST'])
def encrypt_wallet():
    form = QtumPassword()
    if form.validate_on_submit():
        encrypt = qtum("encryptwallet '%s'" % form.passphrase.data)
        if encrypt == None:
            flash('Opps! Something went wrong.', 'error_encrypt')
            return redirect(url_for('setup'))
        flash(encrypt, 'msg')
        time.sleep(2)
        subprocess.run("~/qtum-wallet/bin/qtumd -daemon", shell=True)
        time.sleep(5)
        return redirect(url_for('index'))
    else:
        flash('Passphrase Cannot be Blank!!', 'error_encrypt')
        return redirect(url_for('setup'))

@app.route('/staking_service', methods=['POST'])
def staking_service():
    form = QtumPassword()
    if form.validate_on_submit():
        start_stake = qtum_unlock(form.passphrase.data, 99999999, 'true')
        if start_stake == None:
            flash('Opps! Wallet Passphrase is Incorrect.', 'error_staking')
            return redirect(url_for('setup'))
        flash('Success! Wallet is now Staking.', 'msg')
        return redirect(url_for('setup'))
    else:
        flash('Passphrase Cannot be Blank!!', 'error_staking')
        return redirect(url_for('setup'))

@app.route('/add_node', methods=['POST'])
def add_node():
    form_addnode = AddNode()
    if form_addnode.validate_on_submit():
        addnode = qtum("addnode '%s' 'add'" % form_addnode.nodeaddress.data)
        if addnode == None:
            flash('Opps! Something went wrong', 'error_node')
            return redirect(url_for('setup'))
        flash('Success! Node Added.', 'msg_node')
        return redirect(url_for('setup'))
    else:
        flash('Please Enter a Node Address!', 'error_node')
        return redirect(url_for('setup'))

@app.route('/lock_wallet')
def lock_wallet():
    qtum("walletlock")
    flash('Success! Wallet is Locked', 'msg_node')
    return redirect(url_for('setup'))

@app.route('/offline')
def offline():
    form = QtumPassword()
    return render_template('offline.html', form=form)

@app.route('/start_wallet')
def start_wallet():
    wallet_start_up()
    time.sleep(8)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
