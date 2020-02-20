#!/usr/bin/env python3.6
'''
   Copyright [2020] [Fernando Cavalcanti Jeronymo]

Created on Feb 17, 2020

@author: Fernando Cavalcanti Jeronymo

'''
import os
import re
import sys
import socket
import logging
import requests
from base64 import b64encode
from http.client import HTTPSConnection
from modules.network import iptools

def getOrUpdateLastSavedIP(IPv4, IPv6):
    replace_ip = True
    myip='%s:%s'%(IPv4, IPv6)
    try:
        myipFile = PATH_INSTALL+'/my_ip.txt'
        logging.info('Checking saved IP on [%s]'%(myipFile))
        if(os.path.isfile(myipFile) == True):
            file = open(myipFile, 'r+')
            ip_file = file.read()
            logging.info('Found IP file -> [%s]: %s'%(myipFile, ip_file.strip()))
            if(ip_file.strip() != myip):
                ip_file = re.sub(ip_file.strip(), myip, ip_file)
                file.seek(0)
                file.write(ip_file)
                file.close()
                logging.info('Need to update IP ... new IP saved in [%s]%'(myipFile))
            else:
                replace_ip = False
                logging.info('IP is same as before, no need to update it.')
        else:
            logging.info('create file my_ip.txt')
            file = open(PATH_INSTALL+'/my_ip.txt','w')
            file.write(myip)
            file.close()
    except Exception as ex:
        logging.error(ex)
        logging.error('Could not update [%s]'%(myipFile))
        raise
    return replace_ip

def updateGoogleDomainIP(URL, PAYLOAD):
    try:
        urlReq = URL%(PAYLOAD)
        logging.info('GOOGLE_DOMAINS_URL: ' + urlReq)
        page_response = requests.get(urlReq, timeout=5)
        logging.info('Response: ' + page_response.text)
    except Exception as e:
        logging.warning('Could not set domain: [%s]'%(str(e)))
        print('Could not set domain: [%s]'%(str(e)))
        return False

##############################################################################
# Main function
##############################################################################
def updateGoogleDomain():
    # Retrieve environment variables set by companion shell script
    URL_GOOGLE_DOMAINS = 'https://%(user)s:%(password)s@domains.google.com/nic/update?hostname=%(domain)s&myip=%(ip)s'
    PAYLOAD = {}
    try:
        PAYLOAD['user'] = os.environ['UPDATE_GOOGLE_DOMAINS_USER'].strip()
        PAYLOAD['password'] = os.environ['UPDATE_GOOGLE_DOMAINS_PASSWORD'].strip()
        PAYLOAD['domain'] = os.environ['UPDATE_GOOGLE_DOMAINS_DOMAIN'].strip()
    except KeyError:
        logging.error('One or more environment variables are missing.  UPDATE_GOOGLE_DOMAINS_USER, UPDATE_GOOGLE_DOMAINS_PASSWORD, and UPDATE_GOOGLE_DOMAINS_DOMAIN are mandatory')
        return False

    # Resolve DOMAINS to make sure it exists and can be found
    dns_result = iptools.resolve_domain_with_dns('%(domain)s'%(PAYLOAD))

    # Hostname and IPs
    hostnames = []
    for value in dns_result.values(): hostnames.append(value[0])
    hostnames = list(set(hostnames))
    my_ip_hostname = hostnames[0]
    IPv4 = iptools.get_external_ip_address()
    IPv6 = iptools.get_external_ip_address(family='AF_INET6')
    logging.info('My IP Hostname: [%s], IPv4: [%s] IPv6: [%s]', my_ip_hostname, IPv4, IPv6)

    # Do we need to update it?
    replace_ip = getOrUpdateLastSavedIP(IPv4, IPv6)
    if (not replace_ip):
        return True

    # Upload IPv4
    PAYLOAD['ip'] = IPv4
    updateGoogleDomainIP(URL_GOOGLE_DOMAINS, PAYLOAD)

    ## Upload IPv6
    #PAYLOAD['ip'] = IPv6
    #updateGoogleDomainIP(URL_GOOGLE_DOMAINS, PAYLOAD)

    return True

##############################################################################
# Running it
##############################################################################
if __name__ == "__main__":
    try:
        # Setting up logger
        try:
            PATH_LOGS=os.getenv('UPDATE_GOOGLE_DOMAINS_LOGS','.')
        except KeyError:
            print('log path not found creating in default folder')

        try:
            logging.basicConfig(
                filename=PATH_LOGS+'/updatemyip.log',
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%d/%m/%Y %I:%M:%S %p')
        except:
            logging.basicConfig(
                filename='/tmp/updatemyip.log',
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%d/%m/%Y %I:%M:%S %p')

        try:
            PATH_INSTALL=os.getenv('PATH_INSTALL_SCRIPT_PYTHON_GOOGLE_DOMAINS', '.')
        except Exception:
            logging.warning('not found enviroment PATH_INSTALL_SCRIPT_PYTHON')

        logging.info('--=-- Started')

        # all the magic happens here...
        if ( not updateGoogleDomain() ):
            sys.exit(1)

        logging.info('--=-- Finished')

    except SystemExit as e:
        # this log will just include content in sys.exit
        logging.error(str(e))
        print(str(e))
        # this log will include traceback
        logging.exception('Fail! For more details, check %s'%(logging.getLoggerClass().root.handlers[0].baseFilename))
        print('Fail! For more details, check %s'%(logging.getLoggerClass().root.handlers[0].baseFilename))
        raise
    except:
       print("Unexpected error:", sys.exc_info()[0])
       raise
