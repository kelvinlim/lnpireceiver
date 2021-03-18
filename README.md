# lnpireceiver
a simple flask server to accept json data from a source such as a flutter app.
This is based on code from https://rahmanfadhil.com/flask-rest-api/


The expected format of the posted data is
```json
{
	"studycode": "driving 0.1",
	"data_version": "0.1",
	"guid": "ab1235-x25",
	"data": "[[1,2,3], [4,5,6]]"
}
```
## to post data
```bash
To post data
curl http://160.94.0.29:5000/posts \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"studycode":"driving", "guid": "ab1235-x25", "data_version":"0.1", "data":"[[1,2,3], [4,5,6]]"}'
    
curl http://160.94.0.29:5000/posts -X POST -H "Content-Type: application/json" -d '{"studycode":"driving", "guid": "ab1235-x25", "data_version":"0.1", "data":"[[1,2,3], [4,5,6]]"}'
```
For flutter see:  https://flutter.dev/docs/cookbook/networking/send-data

## to check on the data, only for testing, don't want to
be able to do this in production
```bash
To check on all data
curl http://160.94.0.29:5000/posts


```

## to initialize the  database
```python
$ python
import receiverlnpi
receiverlnpi.db.create_all()
exit()
```

## to start the  server
```
# change the app.config['SQLALCHEMY_DATABASE_URI'] to a correct URI first
python receiverlnpi.py
```

## to create a docker container
```
# run this command in the lnpireceiver directory
sudo docker build -t lnpireceiver .

```

## to run the container
```
# get the info on the container
sudo docker images | grep lnpi
# to run the container on port 5001
# this makes it available at http://localhost:5001/posts 
sudo docker run -p 5001:5001 lnpireceiver
```

## to initialize a virtual environment
```bash
python -m venv venv/flaskrest
source venv/flaskrest/bin/activate
cd lnpireceiver
pip install -r requirements.txt
```

## python example pulling data
```python
import requests
import json

# pull response #18
req = "http://160.94.0.29:5000/posts/18"

response = requests.get(req)
print(response.json()['created_on'])

# load the json in the data field into a python object
d = json.loads(response.json()['data'])
print("length of data list: ", len(d))
```

## another data example with use of dictionary in the data element to make it more machine readable
```json
{
	"studycode": "driving 0.1",
	"data_version": "0.1",
	"guid": "ab1235-x25",
	"data": {
  		"SubjectID": "1235",
		"moves": [
			["time", "pos1", "pos2"],
			[0, 0, 0],
			[20, 0.1, 2.0],
			[30, 0.2, 1.0]
		]
	}
}
```

## sample code to read in the json into a pandas dataframe
```python
import json
import pandas as pd

filename = "sample1.json"
f = open(filename, "r")

# returns JSON object as  
# a dictionary 
d = json.load(f) 

# read the "moves" list into a pandas dataframe
mdata = d["data"]["moves"]
column_names = mdata.pop(0)
df = pd.DataFrame(mdata, columns=column_names)
print(df)
```
## some helpful info for handing datetime with python in json
https://code-maven.com/serialize-datetime-object-as-json-in-python
## generating datetime json with dart
https://codingwithjoe.com/dart-fundamentals-working-with-json-in-dart-and-flutter/
```dart
class Student {
  final String name;
  final String email;
  final DateTime dob;

  Student(this.name, this.email, this.dob);
} 

import 'dart:convert';

  static String toJson(Student s) {
    Map<String, dynamic> map() =>
    {
      'name': s.name,
      'email': s.email,
      'dob': s.dob.toIso8601String()
    };

    String result = jsonEncode(map());
    return result;
  }

```
