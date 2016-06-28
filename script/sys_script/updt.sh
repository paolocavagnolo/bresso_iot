#!/bin/bash
cd /home/pi/Documents
sudo rm -r /home/pi/Documents/techlab_iot
cd /home/pi/Documents
git clone https://github.com/paolocavagnolo/techlab_iot.git
cd techlab_iot/theBrain/
sudo python setup.py develop

echo "copy myself to /bin"
sudo cp /home/pi/Documents/techlab_iot/script/sys_script/updt.sh /bin/
sudo chmod 755 /bin/updt.sh

echo "copy the script to init.d"
sudo cp /home/pi/Documents/techlab_iot/script/goPlot /etc/init.d/
sudo cp /home/pi/Documents/techlab_iot/script/goSync /etc/init.d/
sudo cp /home/pi/Documents/techlab_iot/script/goBot /etc/init.d/
sudo cp /home/pi/Documents/techlab_iot/script/goBrain /etc/init.d/

echo "chmod 755 to all the script"
sudo chmod 755 /etc/init.d/goPlot
sudo chmod 755 /etc/init.d/goSync
sudo chmod 755 /etc/init.d/goBot
sudo chmod 755 /etc/init.d/goBrain

echo "at the boot!"
sudo update-rc.d goPlot defaults
sudo update-rc.d goSync defaults
sudo update-rc.d goBot defaults
sudo update-rc.d goBrain defaults
