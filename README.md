# Qtum Wallet UI for Ubuntu
 Join our Telegram [here.](https://t.me/joinchat/FvYLc1FTsk6qg_wuN9WF8A)

[Demo running on a Raspberry Pi 3](http://110.145.75.228:5000/)  

[A tutorial for setting up a firewall to prevent internet access to the UI](https://steemit.com/qtum/@trevsadev/raspberry-pi-3-firewall-tutorial-for-the-qtum-pi-user-interface-https-github-com-rpiwalletui-qtum-ui-releases)

## Whats New  
The Ui has had a facelift and is now mobile responsive.  
Prompts users to encrypt their wallet if they have not yet done so.  
Wallet.dat download and upload supported.  
Network information stats added.  
Subtract fee from send amount now available.  
Can stop/start the Qtum wallet from the UI  
UI will run on Pi reboot  
The UI checks and installs/updates the latest Qtum Wallet.  

## Please Note  
This Browser UI is meant to run on your LAN only.  
Allowing internet access to the UI puts you at risk of someone gaining accessing to your wallet.  
By default the UI is not accessible from the Internet.  

## Installation  
PLEASE BACKUP YOUR WALLET.DAT FILE BEFORE INSTALLING.  
Run the following commands to install  
This will also install/update the Qtum core wallet so no need to install it first.   

Copy and past the install script below.  
You can see the [ui-setup script here.](https://github.com/rpiwalletui/qtum-ui/blob/master/ui-install)  
```
$ curl -L https://raw.githubusercontent.com/rpiwalletui/qtum-ui/ubuntu/ui-install | bash
```
## Setup the UI as s Service  
Follow this guide if you want the UI to run on startup.  
Create the following file `sudo nano /etc/systemd/system/qtum-ui.service`  
(enter your password if prompted and press `y` to continue) then add the following.
Making sure to replace `USER` with your current user.
```
[Unit]
Description=Qtum Pi UI
After=multi-user.target

[Service]
Type=idle
User=USER
WorkingDirectory=/home/USER/qtum-ui
ExecStart=/usr/bin/python3 /home/USER/qtum-ui/app.py

[Install]
WantedBy=multi-user.target
```
To exit and save the file `Ctrl+x` then `y` then `enter`
Restart systemctl `sudo systemctl daemon-reload`  
Now enable the UI service `sudo systemctl enable qtum-ui.service`
Lastly is to start the UI `sudo systemctl start qtum-ui.service`  

## Issues
UI slow when wallet is scyncing can seem like the UI is not responding.  

## Contributing
Bug reports and pull requests are welcome on GitHub at https://github.com/rpiwalletui/qtum-ui.  
