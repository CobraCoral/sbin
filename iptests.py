#!/usr/bin/env python3.6
import socket
import dns.resolver
import sys
import traceback
from packages.network import iptools

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

#def get_external_ip_address(family='AF_INET', timeout=5):
#    # Providers
#    providers = dict(
#        ip42 = 'http://ip.42.pl/raw',
#        ipify = 'https://api.ipify.org/?format=json',
#        google = 'https://domains.google.com/checkip',
#        jsonip = 'http://ipv4.jsonip.com',
#        httpbin = 'http://httpbin.org/ip',
#        ipv4bot = 'ipv4bot.whatismyipaddress.com',
#        )
#
#    provider = 'jsonip'
#    if family == 'AF_INET6':
#        provider = 'google'
#    providerURL = providers[provider]
#    logging.info('Finding IP from [%s]:[%s]'%(provider, providerURL))
#    page_response = requests.get(providerURL, timeout=timeout)
#    logging.info('IP returned: [%s]:[%s]'%(page_response, page_response.text))
#    return page_response.text
#
#def resolve_domain_with_dns(domain):
#    retVal = {}
#    # Record [A] (IPv4)
#    try:
#        IPv4_hostname, IPv4_aliaslist, IPv4_ipaddrlist = socket.gethostbyname_ex(domain)
#        logging.info('[IPv4] GetHostByName DOMAINS[%s]: [%s]'%(domain, '%s, %s, %s'%(IPv4_hostname, IPv4_aliaslist, IPv4_ipaddrlist)))
#        retVal['IPv4'] = [IPv4_hostname, IPv4_aliaslist, IPv4_ipaddrlist]
#    except socket.gaierror:
#        logging.error('DOMAINS [%s] does not have a [A] record (IPv4).'%(domain))
#
#    # Record [AAAA] (IPv6)
#    try:
#        IPv6_list=[]
#        for result in socket.getaddrinfo(domain, None, socket.AF_INET6, 0):
#            IPv6_list.append(result[-1][0])
#        IPv6_list = list(set(IPv6_list))
#        IPv6_hostname = socket.gethostbyaddr(IPv6_list[0])[0]
#        IPv6_aliaslist = []
#        logging.info('[IPv6] GetHostByName DOMAINS[%s]: [%s]'%(domain, '%s, %s, %s'%(IPv6_hostname, IPv6_aliaslist, IPv6_list)))
#        retVal['IPv6'] = [IPv6_hostname, IPv6_aliaslist, IPv6_list]
#    except socket.gaierror:
#        logging.error('DOMAINS [%s] does not have a [AAAA] record (IPv6).'%(domain))
#    return retVal

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
