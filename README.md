# RPI Qtum Wallet UI

The Qtum Wallet UI has been developed to give Raspberry Pi users a browser interface for interacting with the wallet, much like the Desktop version.  

## Please Note  
We are still working on a mobile-friendly version, at this time the UI is best viewed on a Desktop / Notebook.  
Currently only tested on [RASPBIAN STRETCH.](https://www.raspberrypi.org/downloads/raspbian/)

This Browser UI is meant to run on your LAN only.  
Allowing internet access to the UI puts you at risk of someone gaining accessing to your wallet.  
By default the UI is not accessible from the Internet.  

## Installation  
Run the following commands to install the Pi UI.  
You should already have the qtum-cli wallet installed and running on the Raspberry Pi.   

1 line install, run the following command.  
You can see the [ui-setup script here.](https://github.com/rpiwalletui/qtum-ui/blob/master/ui-setup)  
```
curl -L https://raw.githubusercontent.com/rpiwalletui/qtum-ui/master/ui-setup | bash
```
Or Step by Step.
```
sudo apt-get update
```
```
sudo apt-get -y install python3-pip libv4l-dev libopenjp2-7 libopenjp2-7-dev libtiff5
```
```
pip3 install flask Flask-WTF Flask-QRcode
```
```
wget https://github.com/rpiwalletui/qtum-ui/archive/qtum-piui-0.1.0-beta.tar.gz
```
```
mkdir ~/qtum-ui  
tar --strip 1 -C ~/qtum-ui -xf ~/qtum-piui-0.1.0-beta.tar.gz  
cd ~/qtum-ui
```
To start the UI run.  
```
python3 app.py &
```  
To Access the UI enter the hostname or IP of your Raspberry Pi  
```
http://YOUR_RASPBERRY_PI_LAN_IP:3404
```
Or
````
http://raspberrypi:3404
````

## Usage

TODO: Use cases and example code coming soon.  

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/rpiwalletui/qtum-ui.  
