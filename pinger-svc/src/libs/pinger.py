# -*- coding: utf-8 -*-

# Python
import ping3

# Flask 

# App

def get_ip_status(ip):
    if ping3.ping(ip):
        return True
    return False