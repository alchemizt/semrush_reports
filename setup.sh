#!/bin/bash

echo "Updating and installing dependencies..."
apt-get update && apt-get install -y wget unzip curl chromium-browser chromium-chromedriver

 

# Install Chrome (if not installed)
if ! command -v google-chrome &> /dev/null
then
    echo "Installing Google Chrome..."
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg
    echo 'deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
    apt update && apt install -y google-chrome-stable
fi

# Install ChromeDriver
echo "Installing ChromeDriver..."
LATEST_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$LATEST_VERSION/chromedriver_linux64.zip -P /tmp/
unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm /tmp/chromedriver_linux64.zip
