#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import argparse
import requests
import logging as log

api_url = "https://api.cloudflare.com/client/v4/user/load_balancers/pools"
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

    parser.add_argument('-a', '--add-pool', action='store_true',
                        default=False, help='Add a Load Balancer Monitor')
    parser.add_argument('-l', '--list-pools', action='store_true',
                        default=False, help='List all Load Balancer Monitors')
    parser.add_argument('-r', '--del-pool', type=str,
                        default=None, help='specify a Load Balancer Monitor to \
                        be deleted')
    parser.add_argument('-e', '--edit-pool', type=str, default='endian',
                        help='specify a Load Balancer Monitor to be edited')
    parser.add_argument('-d', '--pool-details', type=str, default=None,
                        help='give more details about a specific Load \
                        Balancer monitor')
    return parser.parse_args()


''' List all balancer monitors '''


def get_pools():
    pool_list = requests.get(api_url, headers=headers)
    print json.dumps(pool_list.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


''' Add a balancer monitor '''


def add_pool(data):
    pool_add = requests.post(api_url, data, headers=headers)
    print json.dumps(pool_add.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


''' List details of a monitor '''


def get_pool_details(pool_id):
    pool_detail = requests.get(api_url+"/"+pool_id, headers=headers)
    print json.dumps(pool_detail.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


''' Delede a monitor by id '''


def del_pool(pool_delete):
    pool_delete = requests.delete(api_url+"/"+pool_delete, headers=headers)
    print json.dumps(pool_delete.json(), sort_keys=True,
                     indent=2, separators=(',', ': '))


def main():
    args = get_arguments()

    if args.list_pools:
        log.info("Taking the load balancer pool lists, please wait...")
        get_pools()
        sys.exit()

    if args.pool_details is not None:
        log.info("Retrieving details for Pool id: " + args.pool_details)
        get_pool_details(args.pool_details)
        sys.exit()

    if args.del_pool is not None:
        log.info("Deleting Pool id: " + args.del_monitor)
        del_pool(args.del_pool)
        sys.exit()

    if args.add_pool:
        name = raw_input("Add a pool name\n")
        listen = raw_input("Insert the list of origins within this pool \
                           (only the address)\n")
        description = raw_input("Add a description for this pool\n")
        monitor_id = raw_input("Insert the Monitor id\n")
        notification_mail = raw_input("Insert an email address for \
                                      notification")
        print "\nOk, got the following:\n", "Name: ", name,
        "\nOrigins: ", listen, "\nDescription: ", description,
        "\nMonitor id: ", monitor_id, "Notification mail: ", notification_mail,
        params = raw_input("Do you confir the following parameters? y/n: ")
        if params == 'y':
            data = json.dumps({"description": description,
                               "\nname": name, "enabled": true,
                               "\nmonitor": monitor_id,
                               "\norigins": [{"name": name, "address": listen,
                                             "enabled": true}],
                               "notification_email": notification_mail})
            add_pool(data)
            sys.exit()
        elif params == 'n':
            sys.exit()
        else:
            print "Reply y/n"
            sys.exit()


if __name__ == "__main__":
    log.basicConfig(stream=sys.stdout, level=log.INFO)
    main()
