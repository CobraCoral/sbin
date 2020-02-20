#!/usr/bin/env python3.6

###################################################################################################
# Imports
# --=-- Standard library imports
import sys
import json
import socket
import logging
import requests
logger = logging.getLogger()
###################################################################################################

def get_external_ip_address(*, family='AF_INET', provider=None, timeout=5):
    '''
        >>> iptools.get_external_ip_address()
        '70.126.90.220'

        >>> iptools.get_external_ip_address('AF_INET6')
        '2603:9000:8d05:4900:25ac:c506:2dc6:73f4'
    '''
    # Local provider response translation helper functions
    def ip_string_processor(val):
        return val
    def ip_dict_string_processor(val):
        return json.loads(val)['ip']
    def origin_dict_string_processor(val):
        return json.loads(val)['origin']
    # actually sending the request over HTTP
    def send_request(url):
        try:
             logger.info('Finding IP from [%s]:[%s]'%(provider, provider_url))
             page_response = requests.get(provider_url, timeout=timeout)
             logger.info('IP returned: [%s]:[%s]'%(page_response, page_response.text))
             return page_response.text
        except requests.exceptions.RequestException as err:
            logger.warning('get_external_ip_address.send_request: provider[%s] url[%s] disconnected... will try the next provider'%(provider, provider_url))
        except:
            e = sys.exc_info()[0]
            logger.error('get_external_ip_address.send_request: %s'%(e))
            return None

    # Providers
    IPv4_providers = dict(
        ip42 = ['http://ip.42.pl/raw', ip_string_processor],
        ipify = ['https://api.ipify.org/?format=json', ip_dict_string_processor],
        jsonip = ['http://ipv4.jsonip.com', ip_dict_string_processor],
        httpbin = ['http://httpbin.org/ip', origin_dict_string_processor],
        ipv4bot = ['http://ipv4bot.whatismyipaddress.com', ip_string_processor],
        )

    IPv6_providers = dict(
        google = ['https://domains.google.com/checkip', ip_string_processor],
        )

    # Choose the right dictionary to use
    provider_dictionary = IPv4_providers
    if family == 'AF_INET6':
        provider_dictionary = IPv6_providers

    # specific provider requested
    if provider:
        provider_url, provider_ip_function = provider_dictionary[provider]
        result_ip = provider_ip_function(send_request(provider_url))
        if not result_ip:
            logger.error('get_external_ip_address: provider [%s] specified, but we could not retrieve an address due to a requests error.'%(provider))

    # no particular provider requested, try each until we succeed
    for provider in provider_dictionary.keys():
        provider_url, provider_ip_function = provider_dictionary[provider]
        result_ip = provider_ip_function(send_request(provider_url))
        if result_ip:
            return result_ip

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
