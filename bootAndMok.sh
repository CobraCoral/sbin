sudo ls /sys/firmware/efi/efivars/Mok*
sudo efibootmgr -v
sudo ls -l /boot/efi/EFI/ubuntu/
#mokutil --test-key ~fcavalcanti/.ssl/MOK.der
#mokutil --enable-validation
#mokutil --sb-state
#mokutil --list-new
#mokutil --list-enrolled

