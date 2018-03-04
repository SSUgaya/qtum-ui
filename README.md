# RPI Qtum Wallet UI APT VERSION ONLY
This for poeple who have installed the qtum wallet using the [instructions here.](https://github.com/qtumproject/qtum/wiki/Installing-Qtum-on-Raspberry-Pi)

The Qtum Wallet UI has been developed to give Raspberry Pi users a browser interface for interacting with the wallet.  
Join our Telegram [here.](https://t.me/joinchat/FvYLc1FTsk6qg_wuN9WF8A)

[Demo running on a Raspberry Pi 3](http://110.145.75.228:5000/)  

[A tutorial for setting up a firewall to prevent internet access to the UI](https://steemit.com/qtum/@trevsadev/raspberry-pi-3-firewall-tutorial-for-the-qtum-pi-user-interface-https-github-com-rpiwalletui-qtum-ui-releases)
## Please Note  
We are still working on a mobile-friendly version, at this time the UI is best viewed on a Desktop / Notebook.  
Currently only tested using a Raspberry Pi 3 running [RASPBIAN STRETCH.](https://www.raspberrypi.org/downloads/raspbian/)

This Browser UI is meant to run on your LAN only.  
Allowing internet access to the UI puts you at risk of someone gaining accessing to your wallet.  
By default the UI is not accessible from the Internet.  

## Installation  
Run the following commands to install the Pi UI.  
You should already have the qtum-cli wallet installed and running on the Raspberry Pi.   

1 line install, run the following command.  
You can see the [ui-setup script here.](https://github.com/rpiwalletui/qtum-ui/blob/master/ui-install)  
```
$ curl -L https://github.com/rpiwalletui/qtum-ui/tree/qtum-pkg/ui-install | bash
```
Or Step by Step.
```
$ sudo apt-get update
$ sudo apt-get -y install python3-pip libv4l-dev libopenjp2-7 libopenjp2-7-dev libtiff5
$ wget https://github.com/rpiwalletui/qtum-ui/releases/download/0.3.0-beta/qtum-ui-0.3.0-beta.tar.gz
$ mkdir ~/qtum-ui  
$ tar --strip 1 -C ~/qtum-ui -xf ~/qtum-ui-0.3.0-beta.tar.gz  
$ cd ~/qtum-ui
$ pip3 install --upgrade -r requirements.txt
```
To start the UI run.  
```
$ python3 app.py &
```  
To stop the UI run.
```
$ pkill -9 python3
```
To Access the UI enter the hostname or IP of your Raspberry Pi  
http://YOUR_RASPBERRY_PI_LAN_IP:3404 or http://raspberrypi:3404

## Usage

TODO: Use cases and example code coming soon.  

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/rpiwalletui/qtum-ui.  
