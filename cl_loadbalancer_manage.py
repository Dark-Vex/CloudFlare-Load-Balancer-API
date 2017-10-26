#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import argparse
import requests
import logging as log

api_url = "https://api.cloudflare.com/client/v4/user/load_balancers/monitors"
api_key = "<insert-apikey>"
email = "<insert-email>"

headers = {'X-Auth-Email': email, 'X-Auth-Key': api_key,
           'Content-Type': 'application/json'}


def get_arguments():
    """parse the argument provided to the script"""

    parser = argparse.ArgumentParser(
        description='Script to manage cloudflare load balancers \
                    through API',
        epilog='copyright Â© - 2017 Fastnetserv',
        usage='python %s -option')

    parser.add_argument('-a', '--add-balancer', action='store_true',
                        default=False, help='Add a Load Balancer')
    parser.add_argument('-l', '--list-balancer', action='store_true',
                        default=False, help='List all Load Balancer')
    parser.add_argument('-r', '--del-balancer', type=str, default=None,
                        help='specify a Load Balancer to be deleted')
    parser.add_argument('-e', '--edit-balancer', type=str, default='endian',
                        help='specify a Load Balancer to be edited')
    parser.add_argument('-d', '--balancer-details', type=str, default=None,
                        help='give more details about a specific \
                        Load Balancer')
    return parser.parse_args()


''' List all balancer balancers '''


def get_balancer():
    balancer_list = requests.get(api_url, headers=headers)
    print json.dumps(balancer_list.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


''' Add a balancer balancer '''


def add_balancer(data):
    balancer_add = requests.post(api_url, data, headers=headers)
    print json.dumps(balancer_add.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


''' List details of a balancer '''


def get_balancer_details(balancer_id):
    balancer_detail = requests.get(api_url+"/"+balancer_id, headers=headers)
    print json.dumps(balancer_detail.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


''' Delede a balancer by id '''


def del_balancer(balancer_delete):
    balancer_delete = requests.delete(api_url+"/"+balancer_delete,
                                      headers=headers)
    print json.dumps(balancer_delete.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


def main():
    args = get_arguments()

    if args.list_balancers:
        log.info("Taking the load balancer balancer lists, please wait...")
        get_balancer()
        sys.exit()

    if args.balancer_details is not None:
        log.info("Retrieving details for balancer id: " +
                 args.balancer_details)
        get_balancer_details(args.balancer_details)
        sys.exit()

    if args.del_balancer is not None:
        log.info("Deleting balancer id: " + args.del_balancer)
        del_balancer(args.del_balancer)
        sys.exit()

    if args.add_balancer:
        description = raw_input("Add a description to this balancer\n")
        hostname = raw_input("Insert the hostname/domain name\n")
        app_id = raw_input("Insert an APP ID\n")
        print "\nOk, got the following:\n", "Description: ", description,
        "\nHostname: ", hostname, "\nAPP_ID: ", app_id, "\n"
        params = raw_input("Do you confir the following parameters? y/n: ")
        if params == 'y':
            data = json.dumps({"type": "https", "description": description,
                               "method": "GET", "path": "/health",
                               "header": {"Host": [hostname],
                                          "X-App-ID": [app_id]}, "timeout": 3,
                               "retries": 2, "interval": 90,
                               "expected_body": "alive",
                               "expected_codes": "2xx"})
            add_balancer(data)
            sys.exit()
        elif params == 'n':
            sys.exit()
        else:
            print "Reply y/n"
            sys.exit()


if __name__ == "__main__":
    log.basicConfig(stream=sys.stdout, level=log.INFO)
    main()
