#!/bin/bash

sudo dpkg --configure -a
sudo apt update && sudo apt-get autoclean && sudo apt-get clean && sudo apt-get autoremove && sudo apt dist-upgrade -y

# sudo vim /etc/systemd/logind.conf
# sudo vim /etc/environment
# sudo vim /etc/systemd/logind.conf
# sudo restart systemd-logind.service
# sudo chmod 777 -R /usr/share/spotify
# sudo apt install tasksel
# sudo tasksel install kubuntu-desktop
# sudo dpkg --configure -a
# sudo apt update
# sudo apt upgrade sddm
# sudo apt-get install sddm
# sudo kubuntu-devel-release-upgrade
# sudo apt update
# sudo apt-get autoclean
# sudo apt-get clean
# sudo apt-get autoremove
# sudo apt --fix-broken install
# sudo apt list --upgradable
# sudo apt upgrade
# sudo apt full-upgrade
# sudo vim /usr/share/initramfs-tools/hooks/plymouth
