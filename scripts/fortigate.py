import requests
import urllib3  # disable security warning for SSL certificate

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # disable security warning for SSL certificate


def config_download(ipaddr, api_token, filename='backup.conf'):
    '''
    input: ipaddr(string) - target ip address of fortigate
    input: api_token(string) - api_token for api user(accprofile should have sysgrp.mnt)
    input: filename(string) - file name of the config to be saved. default backup.conf
    output: True if backup successfule. False if not successful.
    Tested on: Fortigate OnDemand on AWS - FortiOS6.0.4
    '''
    base_url = f'https://{ipaddr}/api/v2/'
    headers = {'Authorization': f'Bearer {api_token}'}
    params = {'scope': 'global'}
    uri = 'monitor/system/config/backup/'

    rep = requests.get(base_url + uri, headers=headers, params=params, verify=False)
    if rep.status_code != 200:
        print(f'Something went wrong. status_code: {rep.status_code}')
        return False
    with open(filename, 'w') as f:
        f.write(rep.text)

    return True
