#!/usr/bin/env python3.6
import socket
import dns.resolver
import sys
import traceback
from modules.network import iptools

if len(sys.argv) < 3:
    print('Usage: %s <address> <record type [A, MX, AAAA, etc]>'%(sys.argv[0]))
    sys.exit(1)

class logging:
    @staticmethod
    def info(val):
        print(val)

    @staticmethod
    def error(val):
        print(val)

address = sys.argv[1]
record_type = sys.argv[2]

result = iptools.resolve_domain_with_dns(address)
print(result)

if record_type == 'A':
    try:
        print('\n\n' + 'socket.gethostbyname_ex')
        hostname, aliaslist, ipaddrlist = socket.gethostbyname_ex(address)
        print('hostname:%s, aliaslist:%s, ipaddrlist:%s'%(hostname, aliaslist, ipaddrlist))
    except Exception as e:
        print('Could not retrieve by socket.gethostbyname_ex: %s'%(str(e)))
        traceback.print_exc(file=sys.stdout)
else:
    print('\n\n' + 'socket.gethostbyname_ex')
    print('Only [A] (IPv4) record types can use socket.gethostbyname_ex')

try:
    print('\n\n' + 'dns.resolver.query')
    ip_list=[]
    result = dns.resolver.query(address, record_type)
    for entry in result:
        ip_list.append(entry)
    ip_list = list(set(ip_list))
    print('%s'%(ip_list))
except Exception as e:
    print('Could not retrieve by dns.resolver.query: %s'%(str(e)))
    traceback.print_exc(file=sys.stdout)

try:
    print('\n\n' + 'socket.getaddrinfo')
    ip_list=[]
    # AF_INET for IPv4, AF_INET6 for IPv6
    family = socket.AF_INET
    if record_type == 'AAAA':
        family = socket.AF_INET6
    for result in socket.getaddrinfo(address, None, family,0):
        ip_list.append(result[-1][0])
    ip_list = list(set(ip_list))
    print('%s'%(ip_list))
except Exception as e:
    print('Could not retrieve by socket.getaddrinfo: %s'%(str(e)))
    traceback.print_exc(file=sys.stdout)
print('\n\n')
