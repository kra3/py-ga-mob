# -*- coding: utf-8 -*-

from random import randint
import re

__author__ = "Arun KR (kra3) <the1.arun@gmail.com>"
__license__ = "Simplified BSD"

RE_IP = re.compile(r'^[\d+]{1,3}\.[\d+]{1,3}\.[\d+]{1,3}\.[\d+]{1,3}$', re.I)
RE_PRIV_IP = re.compile(r'^(?:127\.0\.0\.1|10\.|192\.168\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.)')
RE_LOCALE = re.compile(r'(^|\s*,\s*)([a-zA-Z]{1,8}(-[a-zA-Z]{1,8})*)\s*(;\s*q\s*=\s*(1(\.0{0,3})?|0(\.[0-9]{0,3})))?', re.I)
RE_GA_ACCOUNT_ID = re.compile(r'^(UA|MO)-[0-9]*-[0-9]*$')

def get_32bit_random_num():
    return randint(0, 0x7fffffff)

def is_valid_ip(ip):
    return True if RE_IP.match(str(ip)) else False

def is_private_ip(ip):
    return True if RE_PRIV_IP.match(str(ip)) else False

def validate_locale(locale):
    return RE_LOCALE.findall(str(locale))

def is_valid_google_account(account):
    return True if RE_GA_ACCOUNT_ID.match(str(account)) else False

def generate_hash(tmpstr):
    hash_val = 1

    if tmpstr:
        hash_val = 0
        for ordinal in map(ord, tmpstr[::-1]):
            hash_val = ((hash_val << 6) & 0xfffffff) + ordinal + (ordinal << 14)
            left_most_7 = hash_val & 0xfe00000
            if left_most_7 != 0:
                hash_val ^= left_most_7 >> 21

    return hash_val
