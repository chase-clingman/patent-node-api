#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Make sure we return to where we were
else
  echo "...Using Chrome from cache"
fi

# Download and install ChromeDriver
CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P $STORAGE_DIR/
unzip $STORAGE_DIR/chromedriver_linux64.zip -d $STORAGE_DIR/
rm $STORAGE_DIR/chromedriver_linux64.zip
mv -f $STORAGE_DIR/chromedriver $STORAGE_DIR/chrome/chromedriver
chown root:root $STORAGE_DIR/chrome/chromedriver
chmod 0755 $STORAGE_DIR/chrome/chromedriver

# be sure to add Chrome and Chromedriver location to the PATH as part of your Start Command
# export PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome/:/opt/render/project/.render/chrome/"

# add your own build commands...
