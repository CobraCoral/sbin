#!/bin/bash

export UPDATE_GOOGLE_DOMAINS_LOGS="/var/log/updatemyip"
export UPDATE_GOOGLE_DOMAINS_USER=aRGOICP3TOwUe0ad
export UPDATE_GOOGLE_DOMAINS_PASSWORD=WdDGB8X5BEcVxfvc
export UPDATE_GOOGLE_DOMAINS_DOMAIN=babyyoda.fernandojeronymo.info

/home/fcavalcanti/work/sbin/updatemyip.py

# let monitor know we run 
curl --silent --header 'Content-Type: application/json' -d '{"script":"updatemyip"}' http://localhost:5000/v1/update 1>/dev/null 2>&1
# with httpie
#http -v POST http://localhost:5000/v1/update script=updatemyip

