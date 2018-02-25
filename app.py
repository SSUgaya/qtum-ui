from flask import Flask, render_template, request, flash, url_for, redirect, send_from_directory
from flask_qrcode import QRcode
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DecimalField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, NumberRange
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import time
import json
import os
import subprocess

WALLET_DIR = os.path.expanduser('~/.qtum')
QTUM_PATH = 'qtum-cli'
DONATION_ADDR = 'qtum:QceE7a47byDhFs9wy2c2ZdXz4yfT4RZLJQ?amount=&label=Donation&message=PIUI-Donation'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['WALLET_DIR'] = WALLET_DIR
app.config['QTUM_PATH'] = QTUM_PATH
app.config['DONATION_ADDR'] = DONATION_ADDR

QRcode(app)
Bootstrap(app)

class ImportWallet(FlaskForm):
    wallet = FileField(validators=[FileRequired(),FileAllowed(['dat'], 'Wallet.dat File Only!')])

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

def procedure_call(x='', y='', path=QTUM_PATH):
    process = subprocess.Popen("%s %s %s" % (path, x, y), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = process.communicate()
    if process.returncode != 0:
        return None
    return out

def qtum_info(x='getwalletinfo', y=''):
    call = procedure_call(x,y)
    if call == None:
        return None
    result = str(call,'utf-8')
    parsed_result = json.loads(result)
    return parsed_result

def qtum(x):
    call = procedure_call(x)
    if call == None:
        return None
    result = str(call,'utf-8')
    return result

def immature_coins():
    total_coins = 0
    unspent_coins = qtum_info('listunspent', 0)
    for unspent in unspent_coins:
        if unspent['confirmations'] < 500:
            total_coins += unspent['amount']
    return total_coins

def wallet_checks():
    check_wallet = qtum_info()
    if check_wallet == None:
        return 'Not_Running'
    result = list(check_wallet.keys())
    if 'unlocked_until' not in result:
        return 'Not_Encrypted'
    return 'OK'

def wallet_start_up(a='',b=''):
    start_wallet = 'qtumd -daemon'
    call = procedure_call(a, b, start_wallet)
    if call == None:
        return None
    return call

def qtum_unlock(passwd, duration, stake='false'):
    wallet_unlock = 'walletpassphrase "%s" %d %s' % (passwd, duration, stake)
    call = procedure_call(wallet_unlock)
    if call == None:
        return None
    return call

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
    donation_string = DONATION_ADDR
    return donation_string

def qrcode_format(address, amount, name, msg):
    response = 'qtum:%s?amount=%s&label=%s&message=%s' % (address, amount, name, msg)
    return response

@app.route('/')
def index():
    block_info = qtum_info("getblockchaininfo")
    block_time =  qtum_info("getblock", block_info["bestblockhash"])
    if wallet_checks() != 'OK':
        return redirect(url_for('offline'))
    return render_template('index.html', stake_time=get_time(), time=time, immature_coins=immature_coins(), block_time=block_time["time"], block_info=block_info, qtum_mempool=qtum_info("getmempoolinfo"), qtum_network=qtum_info("getnettotals"), qtum_wallet=qtum_info(), get_current_block=qtum_info("getinfo"), list_tx=qtum_info("listtransactions '*'", 100), wallet_version=qtum("--version"), stake_output=qtum_info("getstakinginfo"))

@app.route('/send', defaults={'selected_address' : ''})
@app.route('/send/<selected_address>', methods=['GET', 'POST'])
def send(selected_address):
    form = SendForm()
    return render_template('send.html', address=selected_address, form=form, last_tx=qtum_info("listtransactions '*'", 100), get_unspent=qtum_info('listunspent', 0), qtum_wallet=qtum_info())

@app.route('/send_qtum', methods=['POST'])
def send_qtum():
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
    return render_template('send.html', form=form, last_tx=qtum_info("listtransactions '*' 100"), get_unspent=qtum_info('listunspent', 0), qtum_wallet=qtum_info())

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

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    wallet_upload = ImportWallet()
    form = QtumPassword()
    form_addnode = AddNode()
    return render_template('settings.html', wallet_upload=wallet_upload, form=form, form_addnode=form_addnode, qtum_wallet=qtum_info("getinfo"), donate_piui=donate_piui())

@app.route('/encrypt_wallet', methods=['POST'])
def encrypt_wallet():
    form = QtumPassword()
    if form.validate_on_submit():
        encrypt = qtum("encryptwallet '%s'" % form.passphrase.data)
        if encrypt == None:
            flash('Opps! Something went wrong.', 'error_encrypt')
            return redirect(url_for('setup'))
        flash(encrypt, 'msg')
        qtum('stop')
        time.sleep(2)
        wallet_start_up()
        time.sleep(8)
        return redirect(url_for('index'))
    else:
        flash('Passphrase Cannot be Blank!!', 'error_encrypt')
        return redirect(url_for('offline'))

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

@app.route('/send_req', defaults={'selected_cmd' : ''})
@app.route('/send_req/<selected_cmd>', methods=['GET'])
def send_req(selected_cmd):
    qtum(selected_cmd)
    time.sleep(1)
    return redirect(url_for('index'))

@app.route('/offline')
def offline():
    form = QtumPassword()
    if wallet_checks() == 'OK':
        return redirect(url_for('index'))
    return render_template('offline.html', form=form, checks=wallet_checks())

@app.route('/start_wallet')
def start_wallet():
    qtum('stop')
    time.sleep(2)
    wallet_start_up()
    time.sleep(10)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    wallet_upload = ImportWallet()
    if wallet_upload.validate_on_submit():
        f = wallet_upload.wallet.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['WALLET_DIR'], filename))
        os.rename(WALLET_DIR+"/"+filename, WALLET_DIR+"/"+"wallet.dat")
        flash('Success! Please restart your wallet.', 'upload_msg')
        return redirect(url_for('setup'))
    flash('Something went wrong please try again', 'upload_error')
    return redirect(url_for('setup'))

@app.route('/download', methods=['GET'])
def download():
    return send_from_directory(app.config['WALLET_DIR'], filename='wallet.dat', as_attachment=True, attachment_filename='wallet_backup.dat')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
