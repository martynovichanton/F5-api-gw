import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import getpass

user = getpass.getpass("Enter user")
password = getpass.getpass("Enter password")
device_ip = "192.168.56.7"
url = "https://" + device_ip + "/mgmt/shared/authn/login"
payload = "{\n    \"username\":" + user + ",\n    \"password\":" + password + ",\n    \"loginProviderName\": \"tmos\"\n}"
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    }

response = requests.request("POST", url, data=payload, headers=headers, verify = False)

token = response.json()['token']['token']


url = "https://" + device_ip + "/mgmt/shared/authz/tokens"
payload = ""
headers = {
    'X-F5-Auth-Token': token,
    'cache-control': "no-cache",
    }

response = requests.request("GET", url, data=payload, headers=headers, verify = False)

#print(response.text)


url = "https://" + device_ip + "/mgmt/shared/authz/tokens/" + token

payload = "{\n    \"timeout\":\"3600\"\n}"
headers = {
    'Content-Type': "application/json",
    'X-F5-Auth-Token': token,
    'cache-control': "no-cache",
    }

response = requests.request("PATCH", url, data=payload, headers=headers, verify = False)

print(response.json()['token'])
print(response.json()['timeout'])
