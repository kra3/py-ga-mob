# -*- coding: utf-8 -*-

from random import randint

__author__ = "Arun KR (kra3) <the1.arun@gmail.com>"
__license__ = "Simplified BSD"

def get32bitRandom():
    return str(randint(0, 0x7fffffff))
