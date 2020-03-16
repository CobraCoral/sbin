echo "======== Dimensions"
xrandr
xdpyinfo  | grep -oP 'dimensions:\s+\K\S+'

echo "======== Video"
sudo lshw -c video
inxi -Fxz -G --display

echo "======== Vendor:"
glxinfo | grep vendor

echo "\n======== lspci VGA:"
lspci -k | grep -A 2 -i "VGA"

echo "\n"
#sudo lspci -nnkvv | less

