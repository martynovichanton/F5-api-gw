from django.urls import path
from . import views


urlpatterns = [
    path('', views.root, name='root'),
    path('getpoolnames/', views.poolnames, name='poolnames'),
    path('getpoolconfig/<pool>', views.poolconfig, name='poolconfig'),
    path('getpoolmembers/<pool>', views.poolmembers, name='poolmembers'),
    path('getpoolmembersfiltered/<pool>', views.poolmembersfiltered, name='poolmembersfiltered'),
    path('getpoolmembersstats/<pool>', views.poolmembersstats, name='poolmembersstats'),
    path('getpoolmembersstatsfiltered/<pool>', views.poolmembersstatsfiltered, name='poolmembersstatsfiltered'),
    path('getpoolmembersstatsfilteredtable/<pool>', views.poolmembersstatsfilteredtable, name='poolmembersstatsfilteredtable'),
    path('getpoolmembersstatsall/', views.poolmembersstatsall, name='poolmembersstatsall'),
    path('getpoolmembersstatsallfiltered/', views.poolmembersstatsallfiltered, name='poolmembersstatsallfiltered'),
    path('getpoolmembersstatsallfilteredtable/', views.poolmembersstatsallfilteredtable, name='poolmembersstatsallfilteredtable'),
    path('gettoken/', views.token, name='token'),
    path('disablemember/<pool>/members/<member>', views.disable_member, name='disable_member'),
    path('enablemember/<pool>/members/<member>', views.enable_member, name='enable_member'),
    path('changememberpriority/<pool>/members/<member>/priority/<prioritygroup>', views.change_member_priority, name='change_member_priority'),


]
