# RPI Qtum Wallet UI

The Qtum Wallet UI has been developed to give Raspberry Pi users a browser interface for interacting with the wallet, much like the Desktop version.  

## Please Note  
We are still working on a mobile friendly version, at this time the UI is best viewed on a Desktop / Notebook.  

This Browser UI is meant to run on your LAN only. Allowing access to the UI from the internet  
puts you at risk of someone accessing your wallet. For security reasons do not open Port 3404

## Installation
Run the following commands to install the Pi UI.  
You should already have the qtum-cli wallet installed and running on the Raspberry Pi.   
```
sudo apt-get update
```
```
sudo apt-get install python3-pip hamlib-dev libasound-dev  libv4l-dev libopenjp2-7 libopenjp2-7-dev libtiff5
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
cd qtum-ui
```
To start the UI run.  
```
python3 app.py &
```  
To Access the UI enter the hostname or IP of your Raspberry Pi
```
http://YOUR_RASPBERRY_PI_IP:3404
```
Or
````
http://raspberrypi:3404
````

## Usage

TODO: Use cases and example code coming soon.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/rpiwalletui/qtum-ui.
