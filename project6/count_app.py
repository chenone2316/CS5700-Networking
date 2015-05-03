#!/usr/bin/python
import os
import sys

apps = ["google", "amazon", "apple", "qq", "163", "netease", "yahoo", "linkedin", "itunes", "icloud"]
count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

file = open("dns_info.txt", "r")
alllines = file.readlines()

for line in alllines:
	for i in range(10):
		if line.find(apps[i]) != -1:
			count[i] += 1

print count
