#!/usr/bin/env python3.6
import json
import socket
from powerline.lib.url import urllib_read

# Providers
ipify = ('ipify', 'https://api.ipify.org/?format=json')
httpbin = ('httpbin', 'http://httpbin.org/ip')
jsonip = ('jsonip', 'http://ipv4.jsonip.com')
ip42 = ('ip42', 'http://ip.42.pl/raw')
baby_yoda = ('baby_yoda', '')

# IP Dictionary
IPs = {}

IPs[ipify[0]] = json.loads(urllib_read(ipify[1]))['ip']
IPs[httpbin[0]] = json.loads(urllib_read(httpbin[1]))['origin']
IPs[jsonip[0]] = json.loads(urllib_read(jsonip[1]))['ip']
IPs[ip42[0]] = urllib_read(ip42[1])
IPs[baby_yoda[0]] = socket.gethostbyname(baby_yoda[1])

print("""
%(ipify)s
%(httpbin)s
%(jsonip)s
%(ip42)s
%(baby_yoda)s
"""%(IPs))
