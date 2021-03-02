#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Example code to read in the driving_task data from the REST API server

@author: kolim
https://www.nylas.com/blog/use-python-requests-module-rest-apis/
import request

Also has section on authentication using access tokens
Oauth

https://www.dataquest.io/blog/python-api-tutorial/

"""

import requests
import json
import dateutil.parser
import pandas as pd

urlServer = "https://x0-29.psych.umn.edu/dend/posts"

response = requests.get(urlServer)

print(response.headers)
entries = response.json()

print("There are ", len(entries), " entries")


# pull response
entry = int(input('Enter entry number: '))
req = "http://160.94.0.29:5000/posts/18"
req = urlServer + '/' + str(entry)

response = requests.get(req)
print(response.json()['created_on'])

d = response.json()['data']
# load the json in the data field into a python object
dd = json.loads(response.json()['data'])

# convert ISO 8601 datetime to python datetime
dtstart = dateutil.parser.parse(dd['StartTime'])
dtend = dateutil.parser.parse(dd['EndTime'])

# read the data into a pandas dataframe with headers
mdata = dd["Moves"]
print("length of data list: ", len(mdata))

column_names = mdata.pop(0)
df = pd.DataFrame(mdata, columns=column_names)
print(df)

print("SubjectID: ", dd['SubjectID'])
print("StartTime: ", dtstart)
print("EndTime: ", dtend)
print("Sensitivity: ", dd['Sensitivity'])
print("Number of moves ", len(mdata))
print("Sensitivity: ", dd['Sensitivity'])
print("TaskVersion: ", dd['TaskVersion'])
print("Platform: ", dd['Platform'])
print("Web: ", dd['Web'])



