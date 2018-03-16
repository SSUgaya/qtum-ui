# RPI Qtum Wallet UI  
The Qtum Wallet UI has been developed to give Raspberry Pi users a browser interface for interacting with the wallet.  
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
Currently only tested using a Raspberry Pi 3 running [RASPBIAN STRETCH.](https://www.raspberrypi.org/downloads/raspbian/)

This Browser UI is meant to run on your LAN only.  
Allowing internet access to the UI puts you at risk of someone gaining accessing to your wallet.  
By default the UI is not accessible from the Internet.  

## Installation  
PLEASE BACKUP YOUR WALLET.DAT FILE BEFORE INSTALLING.  
Run the following commands to install the Pi UI.  
This will also install/update the Qtum core wallet so no need to install it first.   

Copy and past the install script below.
You can see the [ui-setup script here.](https://github.com/rpiwalletui/qtum-ui/blob/master/ui-install)  
NOTE: Installation takes 10-20min if it's a new install.
```
$ curl -L https://raw.githubusercontent.com/rpiwalletui/qtum-ui/master/ui-install | bash
```
To Access the UI enter the hostname or IP of your Raspberry Pi  
http://YOUR_RASPBERRY_PI_LAN_IP:3404 or http://raspberrypi:3404

## Issues
Button does not display on Modal in mobile view  < 414px  
UI slow when wallet is scyncing can seem like the UI is not responding.  

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/rpiwalletui/qtum-ui.  
