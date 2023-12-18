
import flask
import requests
from flask import json
from flask import request
from flask import jsonify
from flask_restful import Resource, Api
import time
from F5 import F5
import getpass
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = flask.Flask(__name__)
api = Api(app)

f = open('config.py','r')
config = json.load(f)
devices = config['devices']
traffic_group_mapping = config['traffic_groups_mapping']
f.close()

print(json.dumps(config, indent=4, sort_keys=False))

def initialize_f5(partition, token):
    if partition == "Common":
        device = traffic_group_mapping["traffic_group_1"]
    if partition == "Partition00":
        device = traffic_group_mapping["traffic_group_1"]
    if partition == "Partition01":
        device = traffic_group_mapping["traffic_group_1"]
    if partition == "Partition02":
        device = traffic_group_mapping["traffic_group_2"]
    if partition == "Partition03":
        device = traffic_group_mapping["traffic_group_3"]
    if partition == "Partition04":
        device = traffic_group_mapping["traffic_group_2"]
    f5 = F5(devices[device], token)
    return f5

def append_pool_stats_by_name(f5_1_func, f5_2_func, pool_names):
    dataset = []
    for pool in pool_names['pool_names']:
        if "Common" in pool:
            device = traffic_group_mapping["traffic_group_1"]
            if "f501" in device:
                dataset.append(f5_1_func(pool))
            if "f502" in device:
                dataset.append(f5_2_func(pool))
        if "Partition01" in pool:
            device = traffic_group_mapping["traffic_group_1"]
            if "f501" in device:
                dataset.append(f5_1_func(pool))
            if "f502" in device:
                dataset.append(f5_2_func(pool))
        if "Partition02" in pool:
            device = traffic_group_mapping["traffic_group_2"]
            if "f501" in device:
                dataset.append(f5_1_func(pool))
            if "f502" in device:
                dataset.append(f5_2_func(pool))
        if "Partition03" in pool:
            device = traffic_group_mapping["traffic_group_3"]
            if "f501" in device:
                dataset.append(f5_1_func(pool))
            if "f502" in device:
                dataset.append(f5_2_func(pool))
        if "Partition04" in pool:
            device = traffic_group_mapping["traffic_group_2"]
            if "f501" in device:
                dataset.append(f5_1_func(pool))
            if "f502" in device:
                dataset.append(f5_2_func(pool))
        time.sleep(1)
    return dataset

def append_vip_stats_by_name(f5_1_func, f5_2_func, vip_names):
    dataset = []
    for vip in vip_names['vip_names']:
        if "Common" in vip:
            device = traffic_group_mapping["traffic_group_1"]
            if "f501" in device:
                dataset.append(f5_1_func(vip))
            if "f502" in device:
                dataset.append(f5_2_func(vip))
        if "Partition01" in vip:
            device = traffic_group_mapping["traffic_group_1"]
            if "f501" in device:
                dataset.append(f5_1_func(vip))
            if "f502" in device:
                dataset.append(f5_2_func(vip))
        if "Partition02" in vip:
            device = traffic_group_mapping["traffic_group_2"]
            if "f501" in device:
                dataset.append(f5_1_func(vip))
            if "f502" in device:
                dataset.append(f5_2_func(vip))
        if "Partition03" in vip:
            device = traffic_group_mapping["traffic_group_3"]
            if "f501" in device:
                dataset.append(f5_1_func(vip))
            if "f502" in device:
                dataset.append(f5_2_func(vip))
        if "Partition04" in vip:
            device = traffic_group_mapping["traffic_group_2"]
            if "f501" in device:
                dataset.append(f5_1_func(vip))
            if "f502" in device:
                dataset.append(f5_2_func(vip))
        time.sleep(1)
    return dataset

class Index(Resource):
    def get(self):
        index = {
            "Options":[
                "/f5api/token - Example: curl -X GET http://URL/f5api/token -H 'Content-Type: application/json' -H 'password: PASSWORD' -H 'user: USER'",
                "/f5api/poolnames - Example: curl -X GET http://URL/f5api/poolnames -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/poolconfig/<pool> - Example: curl -X GET http://URL/f5api/poolconfig/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/poolmembers/<pool> - Example: curl -X GET http://URL/f5api/poolmembers/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/poolmembersfiltered/<pool> - Example: curl -X GET http://URL/f5api/poolmembersfiltered/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/poolmembersstats/<pool> - Example: curl -X GET http://URL/f5api/poolmembersstats/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/poolmembersstatsfiltered/<pool> - Example: curl -X GET http://URL/f5api/poolmembersstatsfiltered/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/poolmembersstatsfilteredtable/<pool> - Example: curl -X GET http://URL/f5api/poolmembersstatsfilteredtable/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/poolmembersstatsall - Example: curl -X GET http://URL/f5api/poolmembersstatsall -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/poolmembersstatsallfiltered - Example: curl -X GET http://URL/f5api/poolmembersstatsallfiltered -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/poolmembersstatsallfilteredtable - Example: curl -X GET http://URL/f5api/poolmembersstatsallfilteredtable -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/disablemember/<pool>/members/<member> - Example: curl -X GET http://URL/f5api/disablemember/~Partition01~POOLNAME/members/~Partition01~MEMBERNAME:PORT -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/enablemember/<pool>/members/<member> - Example: curl -X GET http://URL/f5api//enablemember/~Partition01~POOLNAME/members/~Partition01~MEMBERNAME:PORT -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/memberpriority/<pool>/members/<member>/priority/<prioritygroup> - Example: curl -X GET http://URL/f5api/memberpriority/~Partition01~POOLNAME/members/~Partition01~MEMBERNAME:PORT/PRIORITYGROUP -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/deletenodeconnections/<node>/port/<port> - Example: curl -X GET http://URL/f5api/deletenodeconnections/NODE%25PARTITION/port/PORT -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/deletepersistrecords/<node>/port/<port> - Example: curl -X GET http://URL/f5api/deletepersistrecords/NODE%25PARTITION/port/PORT -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vipnames - Example: curl -X GET http://URL/f5api/vipnames -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vipconfig/<vip> - Example: curl -X GET http://URL/f5api/vipconfig/~Partition01~VIPNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vipstats/<vip> - Example: curl -X GET http://URL/f5api/vipstats/~Partition01~VIPNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vipstatsfiltered/<vip> - Example: curl -X GET http://URL/f5api/vipstatsfiltered/~Partition01~VIPNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vipstatsall - Example: curl -X GET http://URL/f5api/vipstatsall -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vipstatsallfiltered - Example: curl -X GET http://URL/f5api/vipstatsallfiltered -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vippoolstats/<vip> - Example: curl -X GET http://URL/f5api/vippoolstats/~Partition01~VIPNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vippoolstatsfiltered/<vip> - Example: curl -X GET http://URL/f5api/~Partition01~VIPNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vippoolstatsall - Example: curl -X GET http://URL/f5api/vippoolstatsall -H 'Content-Type: application/json' -H 'token: TOKEN'",
                "/f5api/vippoolstatsallfiltered - Example: curl -X GET http://URL/f5api/~vippoolstatsallfiltered -H 'Content-Type: application/json' -H 'token: TOKEN'",
            ]
        }
        return index

####################################################################################################
### POOLs
####################################################################################################

class PoolNames(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                #get the ip of first device
                f5 = F5(devices[list(devices.keys())[0]], request.headers['token'])
                data = f5.pool_names()
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class PoolConfig(Resource):
    def get(self, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = pool.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.pool_config(pool)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class PoolMembers(Resource):
    def get(self, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = pool.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.pool_members(pool)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class PoolMembersFiltered(Resource):
    def get(self, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = pool.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.pool_members_filtered(pool)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class PoolMemberStats(Resource):
    def get(self, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = pool.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.pool_members_stats(pool)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class PoolMemberStatsFiltered(Resource):
    def get(self, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = pool.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.pool_members_stats_filtered(pool)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class PoolMemberStatsFilteredTable(Resource):
    def get(self, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = pool.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.pool_members_stats_filtered_table(pool)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class PoolMemberStatsAll(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                f5_1 = F5(devices[list(devices.keys())[0]], request.headers['token'])
                f5_2 = F5(devices[list(devices.keys())[1]], request.headers['token'])
                f5_1_func = f5_1.pool_members_stats
                f5_2_func = f5_2.pool_members_stats
                pool_names_all = f5_1.pool_names()
                if "Error" in pool_names_all:
                    return {"Error":json.loads(pool_names_all['Error'])['message']}, json.loads(pool_names_all['Error'])['code']
                dataset = append_pool_stats_by_name(f5_1_func, f5_2_func, pool_names_all)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            return {"pool_stats":dataset}
        else:
            return {"Error":"Bad request"}, 400

class PoolMemberStatsAllFiltered(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                f5_1 = F5(devices[list(devices.keys())[0]], request.headers['token'])
                f5_2 = F5(devices[list(devices.keys())[1]], request.headers['token'])
                f5_1_func = f5_1.pool_members_stats_filtered
                f5_2_func = f5_2.pool_members_stats_filtered
                pool_names_all = f5_1.pool_names()
                if "Error" in pool_names_all:
                    return {"Error":json.loads(pool_names_all['Error'])['message']}, json.loads(pool_names_all['Error'])['code']
                dataset = append_pool_stats_by_name(f5_1_func, f5_2_func, pool_names_all)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            return {"pool_stats":dataset}
        else:
            return {"Error":"Bad request"}, 400

class PoolMemberStatsAllFilteredTable(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                f5_1 = F5(devices[list(devices.keys())[0]], request.headers['token'])
                f5_2 = F5(devices[list(devices.keys())[1]], request.headers['token'])
                f5_1_func = f5_1.pool_members_stats_filtered_table
                f5_2_func = f5_2.pool_members_stats_filtered_table
                pool_names_all = f5_1.pool_names()
                if "Error" in pool_names_all:
                    return {"Error":json.loads(pool_names_all['Error'])['message']}, json.loads(pool_names_all['Error'])['code']
                dataset = append_pool_stats_by_name(f5_1_func, f5_2_func, pool_names_all)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            return {"pool_stats":dataset}
        else:
            return {"Error":"Bad request"}, 400

class Token(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'user' in request.headers and 'password' in request.headers:
            try:
                f5 = F5(devices[list(devices.keys())[0]], "")
                data = f5.token(request.headers['user'], request.headers['password'])
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400
            
class DisableMember(Resource):
    def patch(self, pool, member):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = pool.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                response = f5.disable_member(pool, member)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in response:
                return {"Error":json.loads(response['Error'])['message']}, json.loads(response['Error'])['code']
            return response
        else:
            return {"Error":"Bad request"}, 400

class EnableMember(Resource):
    def patch(self, pool, member):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = pool.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                response = f5.enable_member(pool, member)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in response:
                return {"Error":json.loads(response['Error'])['message']}, json.loads(response['Error'])['code']
            return response
        else:
            return {"Error":"Bad request"}, 400

class MemberPriority(Resource):
    def patch(self, pool, member, prioritygroup):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = pool.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                response = f5.member_priority(pool, member, prioritygroup)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in response:
                return {"Error":json.loads(response['Error'])['message']}, json.loads(response['Error'])['code']
            return response
        else:
            return {"Error":"Bad request"}, 400

class DeleteNodeConnections(Resource):
    def post(self, node, port):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = node.split('%')[1]
                f5 = initialize_f5("Partition0" + partition, request.headers['token'])
                response = f5.delete_node_connections(node, port)
                if "Error" in response:
                    return {"Error":json.loads(response['Error'])['message']}, json.loads(response['Error'])['code']
                return response
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
        else:
            return {"Error":"Bad request"}, 400

class DeletePersistRecords(Resource):
    def post(self, node, port):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = node.split('%')[1]
                f5 = initialize_f5("Partition0" + partition, request.headers['token'])
                response = f5.delete_persist_records(node, port)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in response:
                return {"Error":json.loads(response['Error'])['message']}, json.loads(response['Error'])['code']
            return response
        else:
            return {"Error":"Bad request"}, 400


####################################################################################################
### VIPs
####################################################################################################

class VipNames(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                #get the ip of first device
                f5 = F5(devices[list(devices.keys())[0]], request.headers['token'])
                data = f5.vip_names()
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class VipConfig(Resource):
    def get(self, vip):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = vip.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.vip_config(vip)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class VipStats(Resource):
    def get(self, vip):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = vip.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.vip_stats(vip)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class VipStatsFiltered(Resource):
    def get(self, vip):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = vip.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.vip_stats_filtered(vip)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class VipStatsAll(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                f5_1 = F5(devices[list(devices.keys())[0]], request.headers['token'])
                f5_2 = F5(devices[list(devices.keys())[1]], request.headers['token'])
                f5_1_func = f5_1.vip_stats
                f5_2_func = f5_2.vip_stats
                vip_names_all = f5_1.vip_names()
                if "Error" in vip_names_all:
                    return {"Error":json.loads(vip_names_all['Error'])['message']}, json.loads(vip_names_all['Error'])['code']
                dataset = append_vip_stats_by_name(f5_1_func, f5_2_func, vip_names_all)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            return {"vip_stats":dataset}
        else:
            return {"Error":"Bad request"}, 400

class VipStatsAllFiltered(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                f5_1 = F5(devices[list(devices.keys())[0]], request.headers['token'])
                f5_2 = F5(devices[list(devices.keys())[1]], request.headers['token'])
                f5_1_func = f5_1.vip_stats_filtered
                f5_2_func = f5_2.vip_stats_filtered
                vip_names_all = f5_1.vip_names()
                if "Error" in vip_names_all:
                    return {"Error":json.loads(vip_names_all['Error'])['message']}, json.loads(vip_names_all['Error'])['code']
                dataset = append_vip_stats_by_name(f5_1_func, f5_2_func, vip_names_all)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            return {"vip_stats":dataset}
        else:
            return {"Error":"Bad request"}, 400

class VipPoolStats(Resource):
    def get(self, vip):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = vip.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.vip_pool_stats(vip)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class VipPoolStatsFiltered(Resource):
    def get(self, vip):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                partition = vip.split("~")[1]
                f5 = initialize_f5(partition, request.headers['token'])
                data = f5.vip_pool_stats_filtered(vip)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            if "Error" in data:
                return {"Error":json.loads(data['Error'])['message']}, json.loads(data['Error'])['code']
            return data
        else:
            return {"Error":"Bad request"}, 400

class VipPoolStatsAll(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                f5_1 = F5(devices[list(devices.keys())[0]], request.headers['token'])
                f5_2 = F5(devices[list(devices.keys())[1]], request.headers['token'])
                f5_1_func = f5_1.vip_pool_stats
                f5_2_func = f5_2.vip_pool_stats
                vip_names_all = f5_1.vip_names()
                if "Error" in vip_names_all:
                    return {"Error":json.loads(vip_names_all['Error'])['message']}, json.loads(vip_names_all['Error'])['code']
                dataset = append_vip_stats_by_name(f5_1_func, f5_2_func, vip_names_all)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            return {"vip_stats":dataset}
        else:
            return {"Error":"Bad request"}, 400

class VipPoolStatsAllFiltered(Resource):
    def get(self):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            try:
                f5_1 = F5(devices[list(devices.keys())[0]], request.headers['token'])
                f5_2 = F5(devices[list(devices.keys())[1]], request.headers['token'])
                f5_1_func = f5_1.vip_pool_stats_filtered
                f5_2_func = f5_2.vip_pool_stats_filtered
                vip_names_all = f5_1.vip_names()
                if "Error" in vip_names_all:
                    return {"Error":json.loads(vip_names_all['Error'])['message']}, json.loads(vip_names_all['Error'])['code']
                dataset = append_vip_stats_by_name(f5_1_func, f5_2_func, vip_names_all)
            except Exception as e:
                print(f"EXCEPTION: {e}")
                return {"Error":"Bad request"}, 400
            return {"vip_stats":dataset}
        else:
            return {"Error":"Bad request"}, 400




####################################################################################################
### POOLs
####################################################################################################

api.add_resource(Index, '/f5api/')
api.add_resource(PoolNames, '/f5api/poolnames')
api.add_resource(PoolConfig, '/f5api/poolconfig/<pool>')
api.add_resource(PoolMembers, '/f5api/poolmembers/<pool>')
api.add_resource(PoolMembersFiltered, '/f5api/poolmembersfiltered/<pool>')
api.add_resource(PoolMemberStats, '/f5api/poolmembersstats/<pool>')
api.add_resource(PoolMemberStatsFiltered, '/f5api/poolmembersstatsfiltered/<pool>')
api.add_resource(PoolMemberStatsFilteredTable, '/f5api/poolmembersstatsfilteredtable/<pool>')
api.add_resource(PoolMemberStatsAll, '/f5api/poolmembersstatsall')
api.add_resource(PoolMemberStatsAllFiltered, '/f5api/poolmembersstatsallfiltered')
api.add_resource(PoolMemberStatsAllFilteredTable, '/f5api/poolmembersstatsallfilteredtable')
api.add_resource(Token, '/f5api/token')
api.add_resource(DisableMember, '/f5api/disablemember/<pool>/members/<member>')
api.add_resource(EnableMember, '/f5api/enablemember/<pool>/members/<member>')
api.add_resource(MemberPriority, '/f5api/memberpriority/<pool>/members/<member>/priority/<prioritygroup>')
api.add_resource(DeleteNodeConnections, '/f5api/deletenodeconnections/<node>/port/<port>')
api.add_resource(DeletePersistRecords, '/f5api/deletepersistrecords/<node>/port/<port>')

####################################################################################################
### VIPs
####################################################################################################

api.add_resource(VipNames, '/f5api/vipnames')
api.add_resource(VipConfig, '/f5api/vipconfig/<vip>')
api.add_resource(VipStats, '/f5api/vipstats/<vip>')
api.add_resource(VipStatsFiltered, '/f5api/vipstatsfiltered/<vip>')
api.add_resource(VipStatsAll, '/f5api/vipstatsall')
api.add_resource(VipStatsAllFiltered, '/f5api/vipstatsallfiltered')
api.add_resource(VipPoolStats, '/f5api/vippoolstats/<vip>')
api.add_resource(VipPoolStatsFiltered, '/f5api/vippoolstatsfiltered/<vip>')
api.add_resource(VipPoolStatsAll, '/f5api/vippoolstatsall')
api.add_resource(VipPoolStatsAllFiltered, '/f5api/vippoolstatsallfiltered')


if __name__ == '__main__':
    app.run()