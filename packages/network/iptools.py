#!/usr/bin/env python3.6
import socket
import logging
import requests

logger = logging.getLogger()

def get_external_ip_address(family='AF_INET', timeout=5):
    '''
        >>> iptools.get_external_ip_address()
        '70.126.90.220'

        >>> iptools.get_external_ip_address('AF_INET6')
        '2603:9000:8d05:4900:25ac:c506:2dc6:73f4'
    '''
    # Providers
    providers = dict(
        ip42 = 'http://ip.42.pl/raw',
        ipify = 'https://api.ipify.org/?format=json',
        google = 'https://domains.google.com/checkip',
        jsonip = 'http://ipv4.jsonip.com',
        httpbin = 'http://httpbin.org/ip',
        ipv4bot = 'ipv4bot.whatismyipaddress.com',
        )

    provider = 'ip42'
    if family == 'AF_INET6':
        provider = 'google'
    providerURL = providers[provider]
    logger.info('Finding IP from [%s]:[%s]'%(provider, providerURL))
    page_response = requests.get(providerURL, timeout=timeout)
    logger.info('IP returned: [%s]:[%s]'%(page_response, page_response.text))
    return page_response.text

def resolve_domain_with_dns(domain):
    '''
        >>> iptools.resolve_domain_with_dns('fernandojeronymo.info')
        DOMAINS [fernandojeronymo.info] does not have a [AAAA] record (IPv6).
        {'IPv4': ['fernandojeronymo.info', [], ['70.126.90.220']]}

        >>> iptools.resolve_domain_with_dns('babyyoda.fernandojeronymo.info')
        DOMAINS [babyyoda.fernandojeronymo.info] does not have a [A] record (IPv4).
        {'IPv6': ['BABY-YODA', [], ['2603:9000:8d05:4900:25ac:c506:2dc6:73f4']]}
    '''
    retVal = {}
    # Record [A] (IPv4)
    try:
        IPv4_hostname, IPv4_aliaslist, IPv4_ipaddrlist = socket.gethostbyname_ex(domain)
        logger.info('[IPv4] GetHostByName DOMAINS[%s]: [%s]'%(domain, '%s, %s, %s'%(IPv4_hostname, IPv4_aliaslist, IPv4_ipaddrlist)))
        retVal['IPv4'] = [IPv4_hostname, IPv4_aliaslist, IPv4_ipaddrlist]
    except socket.gaierror:
        logger.warning('DOMAINS [%s] does not have a [A] record (IPv4).'%(domain))

    # Record [AAAA] (IPv6)
    try:
        IPv6_list=[]
        for result in socket.getaddrinfo(domain, None, socket.AF_INET6, 0):
            IPv6_list.append(result[-1][0])
        IPv6_list = list(set(IPv6_list))
        IPv6_hostname = socket.gethostbyaddr(IPv6_list[0])[0]
        IPv6_aliaslist = []
        logger.info('[IPv6] GetHostByName DOMAINS[%s]: [%s]'%(domain, '%s, %s, %s'%(IPv6_hostname, IPv6_aliaslist, IPv6_list)))
        retVal['IPv6'] = [IPv6_hostname, IPv6_aliaslist, IPv6_list]
    except socket.gaierror:
        logger.warning('DOMAINS [%s] does not have a [AAAA] record (IPv6).'%(domain))
    return retVal
