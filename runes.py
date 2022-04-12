import requests
import base64

#define these from user client
password = b"Oj0rXeMWm9CbgfvNRIrweg"
port = 55886

#prepare LCU connection
API = 'https://127.0.0.1:' + str(port)
auth = 'Basic ' + base64.b64encode(b'riot:' + password).decode('utf-8')

print(auth)
header = {'Authorization' : auth, }

summoner = API + '/lol-summoner/v1/current-summoner'
r = requests.get(summoner, headers=header, verify=False)

print(r.status_code)
print(r.headers)
print(r.json())


# Accessing the LCU API
