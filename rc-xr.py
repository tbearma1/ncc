#!/usr/bin/env python
#
# Copyright (c) 2018 Cisco and/or its affiliates
#
import sys
import requests
from argparse import ArgumentParser
from requests.auth import HTTPBasicAuth


def send_request(protocol, host, port, url, outputformat, username, password):
    print(url)
    '''Generate a simple RESTCONF request.
    '''
    # url = "{}://{}:{}/restconf/data/Cisco-IOS-XR-ifmgr-cfg:interface-configurations/interface-configuration=act,GigabitEthernet0%2f0%2f0%2f0/description".format(
    url = "{}://{}:{}{}".format(
        protocol, host, port, url)
    try:
        response = requests.get(
            auth=HTTPBasicAuth(username, password),
            url=url,
            headers={ 'Accept': ("application/yang-data+%s" % outputformat), 'Content-Type': ("application/yang-data+%s" % outputformat) },
            verify=False
        )
        #print('Response HTTP Status Code: {status_code}'.format(
        #    status_code=response.status_code))
        #print('Response HTTP Response Body: {content}'.format(
        #    content=response.content))
        print(response.content.decode("utf-8"))
    except requests.exceptions.RequestException:
        print(str('HTTP Request failed'))


if __name__ == '__main__':

    parser = ArgumentParser(description='Do a RESTCONF operation:')

    # Input parameters
    parser.add_argument('--host', type=str, required=True,
                        help="The device IP or DN")
    parser.add_argument('-u', '--username', type=str, default='cisco',
                        help="Go on, guess!")
    parser.add_argument('-U', '--url', type=str, default='/restconf/data/Cisco-IOS-XE-native:native',
                        help="ohhh no man url you know...reallyi not?")
    parser.add_argument('-p', '--password', type=str, default='cisco',
                        help="Yep, this one too! ;-)")
    parser.add_argument('-o', '--outputformat', type=str, default='json',
                        help="can be xml or json...forget something else")
    parser.add_argument('--port', type=int, default=830,
                        help="Specify this if you want a non-default port")

    args = parser.parse_args()

    send_request( "https", args.host, args.port, args.url, args.outputformat, args.username, args.password)
