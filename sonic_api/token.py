

import requests
import json
requests.packages.urllib3.disable_warnings()


def get_token():
  headers = {'Content-Type': 'application/yang-data+json', 'Cache-Control': 'no-cache'}
  data = {'username': "admin", 'password': "admin"}
  auth_resp = requests.post("https://192.168.0.215/authenticate", data=json.dumps(data), headers=headers, verify=False)

  print(auth_resp.json()['access_token'])


get_token()
