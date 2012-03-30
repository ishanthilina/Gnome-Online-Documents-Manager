#!/bin/bash

#crete the directories
mkdir $HOME/.godm
cp -r ./src/* $HOME/.godm
cp ./uninstall.sh $HOME/.godm
cp ./.settings.cfg $HOME

#add the extension to LibreOffice
/usr/lib/libreoffice/program/unopkg add godm.zip

echo "Gnome Online Accounts Manager was installed  successfully....!"
