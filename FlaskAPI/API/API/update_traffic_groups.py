import requests
import json
from Crypto import Crypto
import getpass
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_traffic_groups():
    # get traffic groups
    url = "https://" + device_ip + "/mgmt/tm/cm/traffic-group/"
    traffic_groups = requests.get(url, data=payload, headers=json.loads(crypto.decrypt_random_key(headers)), verify = False)
    traffic_groups_list = []
    #print(traffic_groups.json())
    for tg in traffic_groups.json()['items']:
        if "local-only" not in tg['fullPath']:
            traffic_groups_list.append(tg['fullPath'])
    #print(traffic_groups_list)
    return traffic_groups_list

def update_traffic_groups(traffic_groups_list):
    # get active machine per traffic group
    traffic_group_mapping = {}
    for tg in traffic_groups_list:
        url = "https://" + device_ip + "/mgmt/tm/cm/traffic-group/" + tg.split('/')[2] + "/stats"
        data = requests.get(url, data=payload, headers=json.loads(crypto.decrypt_random_key(headers)), verify = False)
        #print(data.json())
        active_device_traffic_group = ""
        for d in data.json()['entries']:
            if data.json()['entries'][d]['nestedStats']['entries']['failoverState']['description'] == 'active':
                active_device_traffic_group = data.json()['entries'][d]['nestedStats']['entries']['deviceName']['description']
        #print(tg,active_device_traffic_group)
        #traffic groups and device names are written with -
        #need to replace with _
        #remove suffix
        traffic_group_mapping[tg.split('/')[2].replace("-","_")] = active_device_traffic_group.split('/')[2].replace("-","_").replace(".com","").replace(".prod","")

    # print(traffic_group_mapping)
    return traffic_group_mapping



crypto = Crypto()

f = open('config.py','r+')
config = json.load(f)
#get the first device ip
device_ip = config['devices'][list(config['devices'].keys())[0]]

payload = ""
headers = crypto.encrypt_random_key(json.dumps({
            'Content-Type': "application/json",
            'X-F5-Auth-Token': getpass.getpass("token"),
            'cache-control': "no-cache"
        }))

traffic_groups_list = get_traffic_groups()
traffic_group_mapping = update_traffic_groups(traffic_groups_list)

config['traffic_groups_mapping'] = traffic_group_mapping
print(json.dumps(config, indent=4, sort_keys=False))
f.seek(0)
f.write(json.dumps(config, indent=4, sort_keys=False))
f.close()

