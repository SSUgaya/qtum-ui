#!/bin/bash
cd ~ || return
DIR="./qtum-ui"
if [ -d "$DIR" ]
then
  echo Qtum-Ui Already Installed
else
  sudo apt-get update
  sudo apt-get install -y python3-pip libopenjp2-7 libopenjp2-7-dev libtiff5
  mkdir ~/qtum-ui
  echo Downloading Qtum-Ui
  wget https://github.com/rpiwalletui/qtum-ui/archive/qtum-piui-0.1.0-beta.tar.gz
  echo Installing...
  tar --strip 1 -C ~/qtum-ui -xf ~/qtum-piui-0.1.0-beta.tar.gz
  rm qtum-piui-0.1.0-beta.tar.gz
  pip3 install flask Flask-WTF Flask-QRcode
  cd  ~/qtum-ui || return
  python3 app.py &
  sleep 3
fi
echo The UI is now starting.
