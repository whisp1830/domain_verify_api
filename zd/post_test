#! /usr/bin/env
# encoding:utf-8
"""
API test server
================
Author @ WUD
Date @ 2019/06/21
"""

import requests
import time
import hashlib
import json


class test_server_method(object):
    def __init__(self):
        pass

    def post(self, url):
        with open("test_domain.txt", "r") as f:
            domains = f.readlines()

        domains_hash = hashlib.md5("".join(domains)).hexdigest()

        d = {
            "time": time.time(),
            "id": "0000001",
            "file_url": "http://10.236.215.85:8888/verify_dns/t.txt/",
            "file_md5": domains_hash
        }

        # print type(d)
        # d = json.dumps(d)
        # print type(d)
        requests.post(url, json=d)


if __name__ == '__main__':
    url = "http://10.245.146.207:8888/notify/path/domain_list"
    test_server_method().post(url)
