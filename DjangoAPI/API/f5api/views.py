from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . F5 import F5
import getpass
import time
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

device_ip_1 = "10.0.0.14"
device_ip_2 = "10.0.0.14"

@require_http_methods(["GET"])
def root(request):
    root_page = {
        "Options":[
            "/gettoken - Example: curl -X GET http://URL/gettoken -H 'Content-Type: application/json' -H 'password: PASSWORD' -H 'user: USER'",
            "/getpoolnames - Example: curl -X GET http://URL/getpoolnames -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/getpoolconfig/<pool> - Example: curl -X GET http://URL/getpoolconfig/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/getpoolmembers/<pool> - Example: curl -X GET http://URL/getpoolmembers/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/getpoolmembersfiltered/<pool> - Example: curl -X GET http://URL/getpoolmembersfiltered/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/getpoolmembersstats/<pool> - Example: curl -X GET http://URL/getpoolmembersstats/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/getpoolmembersstatsfiltered/<pool> - Example: curl -X GET http://URL/getpoolmembersstatsfiltered/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/getpoolmembersstatsfilteredtable/<pool> - Example: curl -X GET http://URL/getpoolmembersstatsfilteredtable/~Partition01~POOLNAME -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/getpoolmembersstatsall - Example: curl -X GET http://URL/getpoolmembersstatsall -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/getpoolmembersstatsallfiltered - Example: curl -X GET http://URL/getpoolmembersstatsallfiltered -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/getpoolmembersstatsallfilteredtable - Example: curl -X GET http://URL/getpoolmembersstatsallfilteredtable -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/disablemember/<pool>/members/<member> - Example: curl -X GET http://URL//disablemember/~Partition01~POOLNAME/members/~Partition01~MEMBERNAME:PORT -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/enablemember/<pool>/members/<member> - Example: curl -X GET http://URL//enablemember/~Partition01~POOLNAME/members/~Partition01~MEMBERNAME:PORT -H 'Content-Type: application/json' -H 'token: TOKEN'",
            "/changememberpriority/<pool>/members/<member>/priority/<prioritygroup> - Example: curl -X GET http://URL//changememberpriority/~Partition01~POOLNAME/members/~Partition01~MEMBERNAME:PORT/PRIORITYGROUP -H 'Content-Type: application/json' -H 'token: TOKEN'"
        ]
    }
    
    
    return JsonResponse(root_page)

@require_http_methods(["GET"])
def poolnames(request):
    if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
        f5 = F5(device_ip_1, request.headers['Token'])
        data = f5.get_pool_names()
        if "Error" in data:
            return JsonResponse({"Error":"Bad request"}, status=400)
        return JsonResponse(data)
    else:
        return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def poolconfig(request, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            if "Partition01" in pool or "Partition03" in pool or "Common" in pool:
                f5 = F5(device_ip_1, request.headers['token'])
            if "Partition02" in pool or "Partition04" in pool:
                f5 = F5(device_ip_2, request.headers['token'])
            data = f5.get_pool_config(pool)
            if "Error" in data:
                return JsonResponse({"Error":"Bad request"}, status=400)
            return JsonResponse(data)
        else:
            return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def poolmembers(request, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            if "Partition01" in pool or "Partition03" in pool or "Common" in pool:
                f5 = F5(device_ip_1, request.headers['token'])
            if "Partition02" in pool or "Partition04" in pool:
                f5 = F5(device_ip_2, request.headers['token'])
            data = f5.get_pool_members(pool)
            if "Error" in data:
                return JsonResponse({"Error":"Bad request"}, status=400)
            return JsonResponse(data)
        else:
            return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def poolmembersfiltered(request, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            if "Partition01" in pool or "Partition03" in pool or "Common" in pool:
                f5 = F5(device_ip_1, request.headers['token'])
            if "Partition02" in pool or "Partition04" in pool:
                f5 = F5(device_ip_2, request.headers['token'])
            data = f5.get_pool_members_filtered(pool)
            if "Error" in data:
                return JsonResponse({"Error":"Bad request"}, status=400)
            return JsonResponse(data)
        else:
            return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def poolmembersstats(request, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            if "Partition01" in pool or "Partition03" in pool or "Common" in pool:
                f5 = F5(device_ip_1, request.headers['token'])
            if "Partition02" in pool or "Partition04" in pool:
                f5 = F5(device_ip_2, request.headers['token'])
            data = f5.get_pool_members_stats(pool)
            if "Error" in data:
                return JsonResponse({"Error":"Bad request"}, status=400)
            return JsonResponse(data)
        else:
            return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def poolmembersstatsfiltered(request, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            if "Partition01" in pool or "Partition03" in pool or "Common" in pool:
                f5 = F5(device_ip_1, request.headers['token'])
            if "Partition02" in pool or "Partition04" in pool:
                f5 = F5(device_ip_2, request.headers['token'])
            data = f5.get_pool_members_stats_filtered(pool)
            if "Error" in data:
                return JsonResponse({"Error":"Bad request"}, status=400)
            return JsonResponse(data)
        else:
            return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def poolmembersstatsfilteredtable(request, pool):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            if "Partition01" in pool or "Partition03" in pool or "Common" in pool:
                f5 = F5(device_ip_1, request.headers['token'])
            if "Partition02" in pool or "Partition04" in pool:
                f5 = F5(device_ip_2, request.headers['token'])
            data = f5.get_pool_members_stats_filtered_table(pool)
            if "Error" in data:
                return JsonResponse({"Error":"Bad request"}, status=400)
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def poolmembersstatsall(request):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            f5_1 = F5(device_ip_1, request.headers['token'])
            f5_2 = F5(device_ip_2, request.headers['token'])
            pool_names_all = f5_1.get_pool_names()
            if "Error" in pool_names_all:
                return JsonResponse({"Error":"Bad request"}, status=400)
            dataset = []
            for pool in pool_names_all['pool_names']:
                if "Partition01" in pool or "Partition03" in pool or "Common" in pool:
                    dataset.append(f5_1.get_pool_members_stats(pool))
                if "Partition02" in pool or "Partition04" in pool:
                    dataset.append(f5_2.get_pool_members_stats(pool))
                time.sleep(1)
            return JsonResponse({"pools":dataset})
        else:
            return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def poolmembersstatsallfiltered(request):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            f5_1 = F5(device_ip_1, request.headers['token'])
            f5_2 = F5(device_ip_2, request.headers['token'])
            pool_names_all = f5_1.get_pool_names()
            if "Error" in pool_names_all:
                return JsonResponse({"Error":"Bad request"}, status=400)
            dataset = []
            for pool in pool_names_all['pool_names']:
                if "Partition01" in pool or "Partition03" in pool or "Common" in pool:
                    dataset.append(f5_1.get_pool_members_stats_filtered(pool))
                if "Partition02" in pool or "Partition04" in pool:
                    dataset.append(f5_2.get_pool_members_stats_filtered(pool))
                time.sleep(1)
            return JsonResponse({"pools":dataset})
        else:
            return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def poolmembersstatsallfilteredtable(request):
        if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
            f5_1 = F5(device_ip_1, request.headers['token'])
            f5_2 = F5(device_ip_2, request.headers['token'])
            pool_names_all = f5_1.get_pool_names()
            if "Error" in pool_names_all:
                return JsonResponse({"Error":"Bad request"}, status=400)
            dataset = []
            for pool in pool_names_all['pool_names']:
                if "Partition01" in pool or "Partition03" in pool or "Common" in pool:
                    dataset.append(f5_1.get_pool_members_stats_filtered_table(pool))
                if "Partition02" in pool or "Partition04" in pool:
                    dataset.append(f5_2.get_pool_members_stats_filtered_table(pool))
                time.sleep(1)
            return JsonResponse({"pools":dataset})
        else:
            return JsonResponse({"Error":"Bad request"}, status=400)

@require_http_methods(["GET"])
def token(request):
    if request.headers['Content-Type'] == 'application/json' and 'user' in request.headers and 'password' in request.headers:
        f5 = F5(device_ip_1, "")
        data = f5.get_token(request.headers['user'], request.headers['password'])
        if "Error" in data:
            return JsonResponse({"Error":"Bad request"}, status=400)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"Error":"Bad request"}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
def disable_member(request, pool, member):
    if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
        f5 = F5(device_ip_1, request.headers['token'])
        response = f5.disable_member(pool, member)
        if "Error" in response:
            return JsonResponse({"Error":"Bad request"}, status=400)
        return JsonResponse(response)
    else:
        return JsonResponse({"Error":"Bad request"}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
def enable_member(request, pool, member):
    if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
        f5 = F5(device_ip_1, request.headers['token'])
        response = f5.enable_member(pool, member)
        if "Error" in response:
            return JsonResponse({"Error":"Bad request"}, status=400)
        return JsonResponse(response)
    else:
        return JsonResponse({"Error":"Bad request"}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
def change_member_priority(request, pool, member, prioritygroup):
    if request.headers['Content-Type'] == 'application/json' and 'token' in request.headers:
        f5 = F5(device_ip_1, request.headers['token'])
        response = f5.change_member_priority(pool, member, prioritygroup)
        if "Error" in response:
            return JsonResponse({"Error":"Bad request"}, status=400)
        return JsonResponse(response)
    else:
        return JsonResponse({"Error":"Bad request"}, status=400)