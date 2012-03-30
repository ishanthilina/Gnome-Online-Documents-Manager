#!/bin/bash

#the name of the extension
extension_name="godm.zip"

#Remove the LibreOffice plugin entry
find $HOME/.libreoffice/3/user/uno_packages/cache/ -name $extension_name -execdir rm -rf $extension_name  \;

#remove the other plugin files

cd ~
rm -rf ./.godm
rm ./.settings.cfg

echo "Gnome Online Accounts Manager was removed successfully....!"
