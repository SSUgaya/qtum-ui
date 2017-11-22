#!/bin/sh
sudo apt-get update
sudo apt-get install python3-pip -y
sudo apt-get install hamlib-dev libasound-dev  libv4l-dev -y
sudo apt-get install libopenjp2-7 libopenjp2-7-dev -y
sudo apt-get install libtiff5 -y
pip3 install flask
pip3 install Flask-WTF
pip3 install Flask-QRcode
