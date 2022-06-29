import json
from requests import post

url = 'https://www.w3schools.com/python/demopage.php'
myobj = {'somekey': 'somevalue'}

# Opening JSON file
with open('city.json') as json_file:
    data = json.load(json_file)
for p in data:
    pload = {
        "name": p['name']
    }
    r = post('http://192.168.8.101:8000/city/', json=pload)
    print(r.status_code)
