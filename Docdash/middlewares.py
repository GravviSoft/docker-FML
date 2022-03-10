# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
import sys
import urllib
from collections import defaultdict
from urllib.request import urlopen, Request

import requests as requests
import scrapy
import stem

from requests import HTTPError
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

import gzip
import logging

from time import time

from scrapy.http import request, headers
from stem.util.log import get_logger
# import requests
import time
from stem import Signal
from stem.control import Controller

import random


# from rotating_proxies.middlewares import RotatingProxyMiddleware
# from rotating_proxies.expire import Proxies
#
#
#
# class MyRotatingProxiesMiddleware(RotatingProxyMiddleware):
#     def __init__(self, proxy_list, logstats_interval, stop_if_no_proxies, max_proxies_to_try, backoff_base,
#                  backoff_cap, crawler):
#         super().__init__(proxy_list, logstats_interval, stop_if_no_proxies, max_proxies_to_try, backoff_base,
#                          backoff_cap, crawler)
#         self.proxies = MyProxies(self.cleanup_proxy_list(proxy_list), backoff=self.proxies.backoff)
#
#
# class MyProxies(Proxies):
#     def __init__(self, proxy_list, backoff=None):
#         super().__init__(proxy_list, backoff)
#         self.chosen = []
#
#     def get_random(self):
#         available = list(self.unchecked | self.good)
#
#         if not available:
#             return None
#
#         # generate unused proxy list from unchecked+good, excluding already used ones
#         not_picked_yet = [x for x in available if x not in self.chosen]
#         if not not_picked_yet:
#             # if the list is empty, reset the chosen list and generate again
#             # only happens when i completely went through all of the good+unchecked proxies
#             self.chosen = []
#             not_picked_yet = [x for x in available if x not in self.chosen]
#
#         # randomly pick a proxy from the 'good' list
#         chosen_proxy = random.choice(not_picked_yet)
#         # mark as chosen
#         self.chosen.append(chosen_proxy)
#         return chosen_proxy
#
#
# logger = get_logger()
# logger.propagate = False


class UserAgentRotatorMiddlware(UserAgentMiddleware):
    user_agents_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
        'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.26 Safari/537.11',
        'Mozilla/5.0 (Windows NT 6.0) yi; AppleWebKit/345667.12221 (KHTML, like Gecko) Chrome/23.0.1271.26 Safari/453667.1221',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.17 Safari/537.11',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
        'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
        'Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/536.5 (KHTML like Gecko) Chrome/19.0.1084.56 Safari/1EA69',
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.22 (KHTML, like Gecko) Chrome/19.0.1047.0 Safari/535.22',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0',
        'Mozilla/5.0 (Macintosh; AMD Mac OS X 10_8_2) AppleWebKit/535.22 (KHTML, like Gecko) Chrome/18.6.872',
        'Mozilla/5.0 (X11; CrOS i686 1660.57.0) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.46 Safari/535.19',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/11.10 Chromium/18.0.1025.142 Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.11 Safari/535.19',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/17.0.963.65 Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.04 Chromium/17.0.963.65 Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/10.10 Chromium/17.0.963.65 Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/17.0.963.65 Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_4) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.04 Chromium/17.0.963.56 Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.940.0 Safari/535.8',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7ad-imcjapan-syosyaman-xkgi3lqg03!wgz',
        'Mozilla/5.0 (X11; CrOS i686 1193.158.0) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7',
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7xs5D9rRDFpg2g',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.8',
        'Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.6 (KHTML, like Gecko) Chrome/16.0.897.0 Safari/535.6',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2',
        'Mozilla/5.0 (X11; FreeBSD i386) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2',
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.04 Chromium/15.0.871.0 Chrome/15.0.871.0 Safari/535.2', ]

    def __int__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        try:
            self.user_agent = random.choice(self.user_agents_list)
            request.headers.setdefault('User-Agent', self.user_agent)
        except IndexError:
            logging.error("Couldn't fetch the user agent")


class ScrapyFbSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyFbDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class ConnectionManager:
#     def __init__(self):
#         self.new_ip = "0.0.0.0"
#         self.old_ip = "0.0.0.0"
#         self.new_identity()
#
#     @classmethod
#     def _get_connection(self):
#         """
#         TOR new connection
#         """
#         try:
#
#             with Controller.from_port(port=9051) as controller:
#                 controller.authenticate(password='16:89560D2DAD09CB5F60D7AD2A6A3CA06C89CB94A2E89555BB33B6741A21')
#                 controller.signal(Signal.NEWNYM)
#                 controller.close()
#         except stem.SocketError:
#             pass
#
#     @classmethod
#     def requestcity(self, request, response, spider):
#         """
#         Request to URL through local proxy
#         """
#         if response.status != 200:
#             with Controller.from_port(port=9051) as controller:
#                 controller.authenticate(password='16:89560D2DAD09CB5F60D7AD2A6A3CA06C89CB94A2E89555BB33B6741A21')
#                 controller.signal(Signal.NEWNYM)
#                 try:
#                     request = scrapy.Request(request, None, {
#                         'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
#                                       "AppleWebKit/535.11 (KHTML, like Gecko) "
#                                       "Ubuntu/10.10 Chromium/17.0.963.65 "
#                                       "Chrome/17.0.963.65 Safari/535.11"})
#                     return request
#                 except HTTPError as e:
#                     return e.strerror
#         return response
#
#     #
#     # @classmethod
#     # def request(self, request):
#     #     """
#     #     TOR communication through local proxy
#     #     :param url: web page to parser
#     #     :return: request
#     #     """
#     #     try:
#     #         self._set_url_proxy()
#     #         request = scrapy.Request(url, None, {
#     #             'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
#     #                           "AppleWebKit/535.11 (KHTML, like Gecko) "
#     #                           "Ubuntu/10.10 Chromium/17.0.963.65 "
#     #                           "Chrome/17.0.963.65 Safari/535.11"})
#     #         request = scrapy.Request(request)
#     #         return request
#     #     except HTTPError as e:
#     #         return e.strerror
#
#     class ProxyMiddleware(object):
#         def process_request(self, request, spider):
#             request.meta['proxy'] = "http://127.0.0.1:8118"


#

import socket
import urllib3
from stem import Signal
from stem.control import Controller
# 
# with Controller.from_port(port=9051) as controller:
#     controller.authenticate(password="16:7A0120469C58F8B860F85FAB0FE00F3774E6FF1F7C313F7C1DFDC70667#D")
#     print("Success!")
#     controller.signal(Signal.NEWNYM)
#     print("New Tor connection processed")


#
# class ProxyMiddleware(object):
#     def process_request(self, request, spider):
#         request.meta['proxy'] = "http://127.0.0.1:8118"
#
#
#
# class GETIT(object):
#     user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
#     headers={'User-Agent':user_agent}
#
#     # initialize some
#     # holding variables
#     oldIP = "0.0.0.0"
#     newIP = "0.0.0.0"
#     # -*- coding: utf-8 -*-
#
#     # Define here the models for your spider middleware
#     #
#     # See documentation in:
#     # https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#     import logging
#     import random
#     import sys
#     from collections import defaultdict
#
#     import requests as requests
#     import scrapy
#     import stem
#
#     from requests import HTTPError
#     from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
#     from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
#
#     import gzip
#     import logging
#
#     from time import time
#
#     from scrapy.http import request
#     from stem.util.log import get_logger
#     # import requests
#     import time
#     from stem import Signal
#     from stem.control import Controller
#
#     import random
#     from rotating_proxies.middlewares import RotatingProxyMiddleware
#     from rotating_proxies.expire import Proxies
#
#
#     class MyRotatingProxiesMiddleware(RotatingProxyMiddleware):
#         def __init__(self, proxy_list, logstats_interval, stop_if_no_proxies, max_proxies_to_try, backoff_base,
#                      backoff_cap, crawler):
#             super().__init__(proxy_list, logstats_interval, stop_if_no_proxies, max_proxies_to_try, backoff_base,
#                              backoff_cap, crawler)
#             self.proxies = MyProxies(self.cleanup_proxy_list(proxy_list), backoff=self.proxies.backoff)
#
#     class MyProxies(Proxies):
#         def __init__(self, proxy_list, backoff=None):
#             super().__init__(proxy_list, backoff)
#             self.chosen = []
#
#         def get_random(self):
#             available = list(self.unchecked | self.good)
#
#             if not available:
#                 return None
#
#             # generate unused proxy list from unchecked+good, excluding already used ones
#             not_picked_yet = [x for x in available if x not in self.chosen]
#             if not not_picked_yet:
#                 # if the list is empty, reset the chosen list and generate again
#                 # only happens when i completely went through all of the good+unchecked proxies
#                 self.chosen = []
#                 not_picked_yet = [x for x in available if x not in self.chosen]
#
#             # randomly pick a proxy from the 'good' list
#             chosen_proxy = random.choice(not_picked_yet)
#             # mark as chosen
#             self.chosen.append(chosen_proxy)
#             return chosen_proxy
#
#     logger = get_logger()
#     logger.propagate = False
#
#     class UserAgentRotatorMiddlware(UserAgentMiddleware):
#         user_agents_list = [

#
#         ]
#
#         def __int__(self, user_agent=''):
#             self.user_agent = user_agent
#
#         def process_request(self, request, spider):
#             try:
#                 self.user_agent = random.choice(self.user_agents_list)
#                 request.headers.setdefault('User-Agent', self.user_agent)
#             except IndexError:
#                 logging.error("Couldn't fetch the user agent")
#
#     class ScrapyFbSpiderMiddleware(object):
#         # Not all methods need to be defined. If a method is not defined,
#         # scrapy acts as if the spider middleware does not modify the
#         # passed objects.
#
#         @classmethod
#         def from_crawler(cls, crawler):
#             # This method is used by Scrapy to create your spiders.
#             s = cls()
#             crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#             return s
#
#         def process_spider_input(self, response, spider):
#             # Called for each response that goes through the spider
#             # middleware and into the spider.
#
#             # Should return None or raise an exception.
#             return None
#
#         def process_spider_output(self, response, result, spider):
#             # Called with the results returned from the Spider, after
#             # it has processed the response.
#
#             # Must return an iterable of Request, dict or Item objects.
#             for i in result:
#                 yield i
#
#         def process_spider_exception(self, response, exception, spider):
#             # Called when a spider or process_spider_input() method
#             # (from other spider middleware) raises an exception.
#
#             # Should return either None or an iterable of Response, dict
#             # or Item objects.
#             pass
#
#         def process_start_requests(self, start_requests, spider):
#             # Called with the start requests of the spider, and works
#             # similarly to the process_spider_output() method, except
#             # that it doesn’t have a response associated.
#
#             # Must return only requests (not items).
#             for r in start_requests:
#                 yield r
#
#         def spider_opened(self, spider):
#             spider.logger.info('Spider opened: %s' % spider.name)
#
#     class ScrapyFbDownloaderMiddleware(object):
#         # Not all methods need to be defined. If a method is not defined,
#         # scrapy acts as if the downloader middleware does not modify the
#         # passed objects.
#
#         @classmethod
#         def from_crawler(cls, crawler):
#             # This method is used by Scrapy to create your spiders.
#             s = cls()
#             crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#             return s
#
#         def process_request(self, request, spider):
#             # Called for each request that goes through the downloader
#             # middleware.
#
#             # Must either:
#             # - return None: continue processing this request
#             # - or return a Response object
#             # - or return a Request object
#             # - or raise IgnoreRequest: process_exception() methods of
#             #   installed downloader middleware will be called
#             return None
#
#         def process_response(self, request, response, spider):
#             # Called with the response returned from the downloader.
#
#             # Must either;
#             # - return a Response object
#             # - return a Request object
#             # - or raise IgnoreRequest
#             return response
#
#         def process_exception(self, request, exception, spider):
#             # Called when a download handler or a process_request()
#             # (from other downloader middleware) raises an exception.
#
#             # Must either:
#             # - return None: continue processing this exception
#             # - return a Response object: stops process_exception() chain
#             # - return a Request object: stops process_exception() chain
#             pass
#
#         def spider_opened(self, spider):
#             spider.logger.info('Spider opened: %s' % spider.name)
#
#     # class ConnectionManager:
#     #     def __init__(self):
#     #         self.new_ip = "0.0.0.0"
#     #         self.old_ip = "0.0.0.0"
#     #         self.new_identity()
#     #
#     #     @classmethod
#     #     def _get_connection(self):
#     #         """
#     #         TOR new connection
#     #         """
#     #         try:
#     #
#     #             with Controller.from_port(port=9051) as controller:
#     #                 controller.authenticate(password='16:89560D2DAD09CB5F60D7AD2A6A3CA06C89CB94A2E89555BB33B6741A21')
#     #                 controller.signal(Signal.NEWNYM)
#     #                 controller.close()
#     #         except stem.SocketError:
#     #             pass
#     #
#     #     @classmethod
#     #     def requestcity(self, request, response, spider):
#     #         """
#     #         Request to URL through local proxy
#     #         """
#     #         if response.status != 200:
#     #             with Controller.from_port(port=9051) as controller:
#     #                 controller.authenticate(password='16:89560D2DAD09CB5F60D7AD2A6A3CA06C89CB94A2E89555BB33B6741A21')
#     #                 controller.signal(Signal.NEWNYM)
#     #                 try:
#     #                     request = scrapy.Request(request, None, {
#     #                         'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
#     #                                       "AppleWebKit/535.11 (KHTML, like Gecko) "
#     #                                       "Ubuntu/10.10 Chromium/17.0.963.65 "
#     #                                       "Chrome/17.0.963.65 Safari/535.11"})
#     #                     return request
#     #                 except HTTPError as e:
#     #                     return e.strerror
#     #         return response
#     #
#     #     #
#     #     # @classmethod
#     #     # def request(self, request):
#     #     #     """
#     #     #     TOR communication through local proxy
#     #     #     :param url: web page to parser
#     #     #     :return: request
#     #     #     """
#     #     #     try:
#     #     #         self._set_url_proxy()
#     #     #         request = scrapy.Request(url, None, {
#     #     #             'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
#     #     #                           "AppleWebKit/535.11 (KHTML, like Gecko) "
#     #     #                           "Ubuntu/10.10 Chromium/17.0.963.65 "
#     #     #                           "Chrome/17.0.963.65 Safari/535.11"})
#     #     #         request = scrapy.Request(request)
#     #     #         return request
#     #     #     except HTTPError as e:
#     #     #         return e.strerror
#     #
#     #     class ProxyMiddleware(object):
#     #         def process_request(self, request, spider):
#     #             request.meta['proxy'] = "http://127.0.0.1:8118"
#
#     #

# import socket
# import urllib3
# from stem import Signal
#     from stem.control import Controller

# class UserAgentRotatorMiddlware(UserAgentMiddleware):
#     user_agents_list = [
#
#     ]
#
#     def __int__(self, user_agent=''):
#         self.user_agent = user_agent
#
#     def process_request(self, request, spider):
#         try:
#             self.user_agent = random.choice(self.user_agents_list)
#             request.headers.setdefault('User-Agent', self.user_agent)
#         except IndexError:
#             logging.error("Couldn't fetch the user agent")
#
# class ProxyMiddleware(object):
#     def process_request(self, request, spider):
#         # request.meta['proxy'] = "http://127.0.0.1:8118"
#         # self.proxie = self.
#         session = requests.session()
#
#         # TO Request URL with SOCKS over TOR
#         session.proxies = {}
#         session.proxies['http'] = 'socks5h://localhost:9050'
#         session.proxies['https'] = 'socks5h://localhost:9050'
#
#         try:
#             r = session.get('http://httpbin.org/ip')
#             print(r)
#             request.meta['proxy'] = "http://127.0.0.1:8118"
#             proxiyo = r.text
#             print(proxiyo)
#             proxiyo2 = json.loads(proxiyo)
#             if proxiyo2:
#                 request.meta['proxy'] = "http://127.0.0.1:8118"
#             else:
#                 print(proxiyo2['origin'])
#                 pass
#         except Exception as e:
#             print(str(e))
#         # else:
#         #     proxiyo = r.text
#         #     proxiyo2 = json.loads(proxiyo)
#         #     if proxiyo2:
#         #         request.meta['proxy'] = "http://127.0.0.1:8118"
#         #     else:
#         #         print(proxiyo2['origin'])
#         #         pass
#
#     def renew_connection(self):
#         global oldIP, newIP
#         with Controller.from_port(port=9051) as controller:
#             controller.authenticate(password="16:7A0120469C58F8B860F85FAB0FE00F3774E6FF1F7C313F7C1DFDC70667#D")
#             print("Success!")
#             controller.signal(Signal.NEWNYM)
#             print("New Tor connection processed")

# class GETIT(object):
#     user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
#     headers = {'User-Agent': user_agent}
#
#     # initialize some
#     # holding variables
#     oldIP = "0.0.0.0"
#     newIP = "0.0.0.0"
#
#     # how many IP addresses
#     # through which to iterate?
#     nbrOfIpAddresses = 3
#
#     # seconds between
#     # IP address checks
#     secondsBetweenChecks = 2
#
#     def get_current_ip(self):
#         session = requests.session()
#
#         # TO Request URL with SOCKS over TOR
#         session.proxies = {}
#         session.proxies['http'] = 'socks5h://localhost:9050'
#         session.proxies['https'] = 'socks5h://localhost:9050'
#
#         try:
#             r = session.get('http://httpbin.org/ip')
#         except Exception as e:
#             print(str(e))
#         else:
#             proxiyo = r.text
#             proxiyo2 = json.loads(proxiyo)
#             print(proxiyo2['origin'])
#             return r.text
#     def renew_connection(self):
#         with Controller.from_port(port=9051) as controller:
#             controller.authenticate(password="16:7A0120469C58F8B860F85FAB0FE00F3774E6FF1F7C313F7C1DFDC70667#D")
#             print("Success!")
#             controller.signal(Signal.NEWNYM)
#             print("New Tor connection processed")
#
#         time.sleep(30)
#         return get_current_ip()
#

from stem import Signal
from stem.control import Controller
import requests
from scrapy import signals

import requests
from toripchanger import TorIpChanger

import time, socks, socket
from urllib.request import urlopen
from stem import Signal
from stem.control import Controller

import requests
from stem import Signal
from stem.control import Controller


# response = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
# response.text.strip()
# '137.74.171.94'
#
# with Controller.from_port(port=9051) as controller:
#     controller.authenticate(password='my password')
#     controller.signal(Signal.NEWNYM)
#
# response = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
# response.text.strip()
# '87.118.92.43'
# se = requests.get('https://api.myip.com/', proxies={'https': '127.0.0.1:8118'})
# response.json()


class ProxyMiddleware(object):
    # initialize some
    # holding variables
    oldIP = "0.0.0.0"
    newIP = "0.0.0.0"

    # how many IP addresses
    # through which to iterate?
    nbrOfIpAddresses = 3

    # seconds between
    # IP address checks
    secondsBetweenChecks = 2

    # request a URL 
    def request(url):
        # communicate with TOR via a local proxy (privoxy)
        def _set_urlproxy():
            proxy_support = urllib.request.ProxyHandler({"http": "127.0.0.1:8118"})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)

        # request a URL
        # via the proxy
        _set_urlproxy()
        request = Request(url, None, headers)
        return urllib.request.urlopen(request).read()

    # signal TOR for a new connection 
    def renew_connection():
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="my_password")
            controller.signal(Signal.NEWNYM)
            controller.close()

    # cycle through
    # the specified number
    # of IP addresses via TOR 
    for i in range(0, nbrOfIpAddresses):

        # if it's the first pass
        if newIP == "0.0.0.0":
            # renew the TOR connection
            renew_connection()
            # obtain the "new" IP address
            newIP = Request("http://icanhazip.com/")
            print(newIP)
        # otherwise
        else:
            # remember the
            # "new" IP address
            # as the "old" IP address
            oldIP = newIP
            # refresh the TOR connection
            renew_connection()
            # obtain the "new" IP address
            newIP = Request("http://icanhazip.com/")

        # zero the 
        # elapsed seconds    
        seconds = 0

        # loop until the "new" IP address
        # is different than the "old" IP address,
        # as it may take the TOR network some
        # time to effect a different IP address
        while oldIP == newIP:
            # sleep this thread
            # for the specified duration
            time.sleep(secondsBetweenChecks)
            # track the elapsed seconds
            seconds += secondsBetweenChecks
            # obtain the current IP address
            newIP = Request("http://icanhazip.com/")
            # signal that the program is still awaiting a different IP address
            print("%d seconds elapsed awaiting a different IP address." % seconds)
        # output the
        # new IP address
        print("")
        print("newIP: %s" % newIP)


#
#
#     def process_request(self, request, spider):
#         with Controller.from_port(port=9051) as controller:
#             controller.authenticate(password="16:7A0120469C58F8B860F85FAB0FE00F3774E6FF1F7C313F7C1DFDC70667")
#             controller.signal(Signal.NEWNYM)
#
#             newIP = urlopen("http://icanhazip.com").read().decode("utf-8")
#             print("NewIP Address: %s" % newIP)
#             request.meta['proxy'] = '127.0.0.1:8118'
#             if controller.is_newnym_available() == False:
#                 print("Waitting time for Tor to change IP: " + str(controller.get_newnym_wait()) + " seconds")
#                 time.sleep(controller.get_newnym_wait())
#             else:
#                 tor_ip_changer = TorIpChanger(tor_password="16:7A0120469C58F8B860F85FAB0FE00F3774E6FF1F7C313F7C1DFDC70667", tor_port=9051,
#                                               local_http_proxy='127.0.0.1:8118')
#                 tor_ip_changer.get_new_ip()
#                 print(tor_ip_changer.get_new_ip())
#                 request.meta['proxy'] = tor_ip_changer.get_new_ip()
#             controller.close()
# # response = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
# # print(response.text.strip())
# #
# # with Controller.from_port(port=9051) as controller:
# #      controller.authenticate(password='my password')
# #      controller.signal(Signal.NEWNYM)
# #
# # response = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
# # print(response.text.strip())
# #
# # response = requests.get('https://api.myip.com/', proxies={'https': '127.0.0.1:8118'})
# # print(response.json())
# #
# # class ProxyMiddleware(object):  # ProxyMiddleware_try_with_print(object):#
# #
# #     def process_request(self, request, spider):
# #         # set_new_ip()
# #         # request.meta['proxy'] = 'http://127.0.0.1:8118'
# #
# #         tor_ip_changer = TorIpChanger(tor_password='my password', tor_port=9051, local_http_proxy='127.0.0.1:8118')
# #         tor_ip_changer.get_new_ip()
# #         print(tor_ip_changer.get_new_ip())
# #         request.meta['proxy'] = tor_ip_changer.get_new_ip()
# #
# #


class GETIT(object):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}

    # initialize some
    # holding variables
    oldIP = "0.0.0.0"
    newIP = "0.0.0.0"

    # how many IP addresses
    # through which to iterate?
    nbrOfIpAddresses = 3

    # seconds between
    # IP address checks
    secondsBetweenChecks = 2

    def get_current_ip(self):
        url = 'http://httpbin.org/ip'
        s = requests.session()
        s.proxies['http'] = 'socks5://127.0.0.1:9050'
        s.proxies['https'] = 'socks5://127.0.0.1:9050'

        print(s.proxies)
        print(requests.get(url, proxies=s).text)
        return s.proxies

    # signal TOR for a new connection
    def renew_connection():
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password='my_password')
            controller.signal(Signal.NEWNYM)
            controller.close()
#
# def retreve_ip():
#     url = 'http://httpbin.org/ip'
#     s = requests.session()
#     s.proxies['http'] = 'socks5://127.0.0.1:9050'
#     s.proxies['https'] = 'socks5://127.0.0.1:9050'
#
#     print(s.proxies)
#     print(requests.get(url, proxies=s).text)
#     return s.proxies
#
#
# def set_new_ip():
#     with Controller.from_port(port=9051) as controller:
#         controller.authenticate(password="16:7A0120469C58F8B860F85FAB0FE00F3774E6FF1F7C313F7C1DFDC70667")
#         controller.signal(Signal.NEWNYM)
#
#
# class ProxyMiddleware(object):  # ProxyMiddleware_try_with_print(object):#
#
#     def process_request(self, request, spider):
#         set_new_ip()
#         request.meta['proxy'] = 'http://127.0.0.1:8118'
#         '''
#         > short version: replace everything in this def by:
#         set_new_ip()
#         request.meta['proxy'] = 'http://127.0.0.1:8118'
#
#         > long verion :
#         the print display the IP address, to show that Tor change it
#         '''
#
#
# # sudo docker run -e COMMANDER_PASSWORD="" -e PROVIDERS_AWSEC2_ACCESSKEYID='AKIAYCBDUMFYYR36ZB4R' -e PROVIDERS_AWSEC2_SECRETACCESSKEY='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'  -it -p 8888:8888 -p 8889:8889 fabienvauchelles/scrapoxy"
#
# import socks
# import socket
#
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, "127.0.0.1", 1080)
#
#
# def create_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
#                       source_address=None, socket_options=None):
#     """Connect to *address* and return the socket object.
#
#     Convenience function.  Connect to *address* (a 2-tuple ``(host,
#     port)``) and return the socket object.  Passing the optional
#     *timeout* parameter will set the timeout on the socket instance
#     before attempting to connect.  If no *timeout* is supplied, the
#     global default timeout setting returned by :func:`getdefaulttimeout`
#     is used.  If *source_address* is set it must be a tuple of (host, port)
#     for the socket to bind as a source address before making the connection.
#     An host of '' or port 0 tells the OS to use the default.
#     """
#
#     host, port = address
#     if host.startswith('['):
#         host = host.strip('[]')
#     err = None
#     for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
#         af, socktype, proto, canonname, sa = res
#         sock = None
#         try:
#             sock = socks.socksocket(af, socktype, proto)
#
#             # If provided, set socket level options before connecting.
#             # This is the only addition urllib3 makes to this function.
#             urllib3.util.connection._set_socket_options(sock, socket_options)
#
#             if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
#                 sock.settimeout(timeout)
#             if source_address:
#                 sock.bind(source_address)
#             sock.connect(sa)
#             return sock
#
#         except socket.error as e:
#             err = e
#             if sock is not None:
#                 sock.close()
#                 sock = None
#
#     if err is not None:
#         raise err
#
#     raise socket.error("getaddrinfo returns an empty list")
#
#
# # monkeypatch
# urllib3.util.connection.create_connection = create_connection
