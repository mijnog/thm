#!/bin/bash
#tun0 ip
ip -4 addr show tun0 | grep -oP 'inet \K[\d.]+'

