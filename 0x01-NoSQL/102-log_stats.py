#!/usr/bin/env python3
'''contains function that imporves 12-log_stats by adding
10 of the most present ips
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''function prints stats about Nginx request logs.
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for m in methods:
        req_count = len(list(nginx_collection.find({'method': m})))
        print('\tmethod {}: {}'.format(m, req_count))
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()
