#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import argparse
import requests
import logging as log

api_url = "https://api.cloudflare.com/client/v4/user/load_balancers/monitors"
api_key = "<your-apikey>"
email = "<your-email>"

headers = {'X-Auth-Email': email, 'X-Auth-Key': api_key,
           'Content-Type': 'application/json'}


def get_arguments():
    """parse the argument provided to the script"""

    parser = argparse.ArgumentParser(
        description='Script to manage cloudflare load balancers \
                    through API',
        epilog='copyright Â© - 2017 Fastnetserv',
        usage='python %s -option')

    parser.add_argument('-a', '--add-monitor', action='store_true',
                        default=False, help='Add a Load Balancer Monitor')
    parser.add_argument('-l', '--list-monitors', action='store_true',
                        default=False, help='List all Load Balancer Monitors')
    parser.add_argument('-r', '--del-monitor', type=str, default=None,
                        help='specify a Load Balancer Monitor to be deleted')
    parser.add_argument('-e', '--edit-monitor', type=str, default='endian',
                        help='specify a Load Balancer Monitor to be edited')
    parser.add_argument('-d', '--monitor-details', type=str, default=None,
                        help='give more details about a specific \
                        Load Balancer monitor')
    return parser.parse_args()


''' List all balancer monitors '''


def get_monitor():
    monitors_list = requests.get(api_url, headers=headers)
    print json.dumps(monitors_list.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


''' Add a balancer monitor '''


def add_monitor(data):
    monitor_add = requests.post(api_url, data, headers=headers)
    print json.dumps(monitor_add.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


''' List details of a monitor '''


def get_monitor_details(monitor_id):
    monitor_detail = requests.get(api_url+"/"+monitor_id, headers=headers)
    print json.dumps(monitor_detail.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


''' Delede a monitor by id '''


def del_monitor(monitor_delete):
    monitor_delete = requests.delete(api_url+"/"+monitor_delete,
                                     headers=headers)
    print json.dumps(monitor_delete.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


def main():
    args = get_arguments()

    if args.list_monitors:
        log.info("Taking the load balancer monitor lists, please wait...")
        get_monitor()
        sys.exit()

    if args.monitor_details is not None:
        log.info("Retrieving details for Monitor id: " + args.monitor_details)
        get_monitor_details(args.monitor_details)
        sys.exit()

    if args.del_monitor is not None:
        log.info("Deleting Monitor id: " + args.del_monitor)
        del_monitor(args.del_monitor)
        sys.exit()

    if args.add_monitor:
        description = raw_input("Add a description to this monitor\n")
        hostname = raw_input("Insert the hostname/domain name\n")
        app_id = raw_input("Insert an APP ID\n")
        print "\nOk, got the following:\n", \
              "Description: ", description, "\nHostname: ", hostname, \
              "\nAPP_ID: ", app_id, "\n"
        params = raw_input("Do you want to configure "
                           "the following parameters? y/n: ")
        if params == 'y':
            data = json.dumps({"type": "https", "description": description,
                               "method": "GET", "path": "/health",
                               "header": {"Host": [hostname],
                                          "X-App-ID": [app_id]}, "timeout": 3,
                               "retries": 2, "interval": 90,
                               "expected_body": "alive",
                               "expected_codes": "2xx"})
            add_monitor(data)
            sys.exit()
        elif params == 'n':
            sys.exit()
        else:
            print "Reply y/n"
            sys.exit()


if __name__ == "__main__":
    log.basicConfig(stream=sys.stdout, level=log.INFO)
    main()
