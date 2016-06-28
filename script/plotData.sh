#!/bin/bash
PTH=`pwd`
echo "Take data from buffer file and manage it, then truncate the file"
cd /home/pi/Documents/techlab_iot/script/
python plotEnergy.py

echo "Copy file to the apache server index.html"
sudo cp panel.html /var/www/html/
cd /var/www/html/
sudo rm index.html
sudo mv panel.html index.html

echo "Starting from a new file"
cd /home/pi/Documents/script/html/
rm panel.html
cp panel_init.html panel.html

echo "come back"
cd $PTH
