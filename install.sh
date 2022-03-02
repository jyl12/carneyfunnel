#!/bin/bash

echo "Installing..."
sudo apt-get update -y
sudo apt-get install libxml2-dev libxmlsec1-dev libffi-dev
sudo pip3 install cryptography
sudo pip3 install freeopcua
pip3 install -r requirements.txt
echo "Installation completed."
