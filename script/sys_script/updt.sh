#!/bin/bash
cd /home/pi/Documents
sudo rm -r /home/pi/Documents/bresso_iot
cd /home/pi/Documents
git clone https://github.com/paolocavagnolo/bresso_iot.git
cd bresso_iot/theBrain/
sudo python setup.py develop

echo "copy myself to /bin"
sudo cp /home/pi/Documents/bresso_iot/script/sys_script/updt.sh /bin/
sudo chmod 755 /bin/updt.sh

echo "copy the script to init.d"
sudo cp /home/pi/Documents/bresso_iot/script/goBrain /etc/init.d/

echo "chmod 755 to all the script"
sudo chmod 755 /etc/init.d/goBrain

echo "at the boot!"
sudo update-rc.d goBrain defaults
