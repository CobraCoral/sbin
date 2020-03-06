#!/bin/bash

sudo apt autoremove
sudo apt-get update
sudo apt-get -y upgrade
#sudo apt-get install -y python3-pip
#sudo apt-get install build-essential libssl-dev libffi-dev python-dev

# If pip3 is coredumping, run it like this:
# pip3 install yowsup --no-binary :all:
