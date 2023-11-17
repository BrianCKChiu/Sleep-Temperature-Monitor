#!/bin/sh

# raspi setup and config script
if [ "$EUID" -ne 0 ]
  then echo "Script needs to be run as root."
  exit
fi

# check for internet connectivity
if ! nc -zw1 google.com 443; then
  echo "No internet connection. Please connect to the internet and try again."
  exit
fi


# update and upgrade
sudo apt-get update
sudo apt-get upgrade

# check if git is installed
if ! command -v git &> /dev/null
then
    # install git
    sudo apt-get install git
fi


sudo apt-get install python 3.11
sudo apt install python3-pip


# change directory to home
cd /home

# clone repo or update repo
if [ -d "/home/Sleep-Temperature-Monitor" ]
then
    cd Sleep-Temperature-Monitor
    git checkout main
    git pull
else
    git clone https://github.com/BrianCKChiu/Sleep-Temperature-Monitor.git
    cd Sleep-Temperature-Monitor
    exit
fi
#  install and/or update requirements
pip3 install -r requirements.txt


# check if variable is passed in
if [ -z "$1" ] || [ "$1" != "server" ] && [ "$1" != "client" ]
  then
    echo "Missing or invalid arguments for install type. Please specify either 'server' or 'client'. \nExample: \n./setup.sh [server | client]"
    exit
fi

if [ "$1" == "server" ]
  then
  # start python script
  python3 ./server/app.py
else
  python3 ./client/app.py



