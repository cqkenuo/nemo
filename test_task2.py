#!/usr/bin/env python3
# coding:utf-8
import time
from nemo.core.tasks.taskapi import TaskAPI

taskapi = TaskAPI()

def test_portscan1():
    options = {'target':['202.101.77.200',],'port':'--top-ports 1000',
            'org_id':9,'rate':1000,'ping':False,'tech':'-sS','iplocation':True,'webtitle':True
            }
    fofasearch = True
    #taskapi.start_task('portscan',kwargs ={'options':options})
    if fofasearch:
        taskapi.start_task('fofasearch',kwargs = {'options':options})
    

def test_domainscan():
    options = {'target':['csg.cn',],
            'org_id':9,'subdomain':True,'webtitle':False,'fofasearch':True,'portscan':False
            }
    taskapi.start_task('domainscan',kwargs ={'options':options})
    fofasearch = True
    if fofasearch:
        taskapi.start_task('fofasearch',kwargs = {'options':options})


def test_portscan():
    options = {'target':['192.168.3.0/24',],'port':'--top-ports 1000',
            'org_id':38,'rate':5000,'ping':True,'tech':'-sS','iplocation':False,'webtitle':True
            }
    fofasearch = False
    taskapi.start_task('portscan',kwargs ={'options':options})
    if fofasearch:
        taskapi.start_task('fofasearch',kwargs = {'options':options})
    

test_portscan()
#test_domainscan()