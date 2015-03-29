#!/usr/bin/python3
import json

with open("medlemmer.json","r") as medlemsfil:
    medlemmer=json.load(medlemsfil)

for medlem in medlemmer:
    if medlem['kommune'] != 'Oslo':
        continue
    print("{bydel}: {navn} <{epost}>".format(**medlem))
