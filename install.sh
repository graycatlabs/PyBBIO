#!/bin/sh
# Install script for PyBBIO v0.2
# May require root priveledges.

PYTHON_PATH="/usr/lib/python2.7"
BBIO="bbio.py"
CONFIG_DIR="$HOME/.pybbio"
CONFIG_FILE="beaglebone.cfg"
CONFIG_FILE_DIR="config"

help() 
{
cat <<EndOfHelp
PyBBIO Installer
 To install/update: sh install.sh -i
 To uninstall: sh install.sh -u
 Display this message: sh install.sh -h
EndOfHelp
exit 0
}

if [ $# -eq 0 ] || [ $1 = "-h" ]; then
  help
fi

if [ $1 = "-u" ]; then
  echo "Uninstalling... PyBBIO"
  if [ -f "$PYTHON_PATH/$BBIO" ]; then
    rm $PYTHON_PATH/$BBIO
  fi
  if [ -d "$CONFIG_DIR" ]; then
    if [ -d "$CONFIG_DIR/config.old/" ]; then    
      rm $CONFIG_DIR/config.old/*.*
      rmdir $CONFIG_DIR/config.old/
    fi
    rm $CONFIG_DIR/*.*
    rmdir $CONFIG_DIR
  fi
  echo "PyBBIO uninstalled successfully"
  exit 0
fi

if [ $1 = "-i" ]; then
  if [ -f "$PYTHON_PATH/$BBIO" ]; then 
    echo "Updating PyBBIO..."
    rm $PYTHON_PATH/$BBIO
  else 
    echo "Installing PyBBIO..."
  fi
  cp $BBIO $PYTHON_PATH/$BBIO

  if [ ! -d "$CONFIG_DIR" ]; then
    echo "Config directory not found..."
    mkdir $CONFIG_DIR
    echo "Created config directory: $CONFIG_DIR"
  else 
    echo "Config directory found..."
  fi

  if [ -f "$CONFIG_DIR/$CONFIG_FILE" ]; then
    if ! diff $CONFIG_DIR/$CONFIG_FILE $CONFIG_FILE_DIR/$CONFIG_FILE > /dev/null; 
    then 
      echo "Backing up old config file..."
      if [ ! -d "$CONFIG_DIR/config.old/" ]; then
        mkdir $CONFIG_DIR/config.old/
      fi
      STAMP=$(date +"%F_%H-%M")
      BACKUP="$STAMP-$CONFIG_FILE"
      mv $CONFIG_DIR/$CONFIG_FILE $CONFIG_DIR/config.old/$BACKUP
    fi
  fi 
  echo "Copying new config file..."
  cp $CONFIG_FILE_DIR/$CONFIG_FILE $CONFIG_DIR
  echo "PyBBIO installed successfully"
  exit 0
fi

help