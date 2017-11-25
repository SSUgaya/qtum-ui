#!/bin/bash
cd ~
directory="~/qtum-ui"
if [ -d "$directory" ]
then
    echo Qtum-Ui Already Installed
else
    sudo apt-get update
    sudo apt-get install python3-pip hamlib-dev libasound-dev  libv4l-dev libopenjp2-7 libopenjp2-7-dev libtiff5
    mkdir ~/qtum-ui
    echo Downloading Qtum-Ui
    wget -O https://github.com/rpiwalletui/qtum-ui/archive/qtum-piui-0.1.0-beta.tar.gz
    echo Installing...
    tar --strip 1 -C ~/qtum-ui -xf ~/qtum-piui-0.1.0-beta.tar.gz
    rm qtum-piui-0.1.0-beta.tar.gz
    pip3 install flask Flask-WTF Flask-QRcode
    cd ~/qtum-ui
    python3 app.py &
fi
echo The UI is now starting.
