#!/usr/bin/zsh
echo "=== LSHW"
sudo lshw
echo "=== dmidecode"
sudo dmidecode
echo "=== lscpu"
lscpu
echo "=== neofetch"
neofetch --config ~/work/dotfiles/.neofetch_config
