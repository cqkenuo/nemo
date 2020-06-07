#!/usr/bin/env python3
# coding:utf-8

from celery import Celery, Task
from .nmap import Nmap
from .ipdomain import IpDomain
from .webtitle import WebTitle
from .portscan import PortScan
from .fofa import Fofa
from .subdomain import SubDmain
from .domainscan import DomainScan

celery_app = Celery('nemo', broker='amqp://', backend='rpc://')


class UpdateTaskStatus(Task):
    '''在celery的任务异步完成时，显示完成状态和结果
    '''

    def on_success(self, retval, task_id, args, kwargs):
        print('task {} done: {}'.format(task_id, retval))
        return super(UpdateTaskStatus, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('task {} fail, reason: {}'.format(task_id, exc))
        return super(UpdateTaskStatus, self).on_failure(exc, task_id, args, kwargs, einfo)


@celery_app.task(base=UpdateTaskStatus)
def add(x, y):
    '''test
    '''
    import time
    import random
    r = random.randint(1, 30)
    time.sleep(r)


TASK_ACTION = {
    'nmap':         Nmap().run,
    'iplocation':   IpDomain().run_iplocation,
    'webtitle':   WebTitle().run,
    'domainip':   IpDomain().run_domainip,
    'portscan':   PortScan().run,
    'fofasearch':   Fofa().run,
    'subdomain':   SubDmain().run,
    'domainscan':   DomainScan().run,
}


def new_task(action, options):
    '''开始一个任务
    '''
    if action in TASK_ACTION:
        task_run = TASK_ACTION.get(action)
        result = task_run(options)
        return result
    else:
        return {'status': 'fail', 'msg': 'no task'}


@celery_app.task(base=UpdateTaskStatus)
def nmap(options):
    '''调用nmap进行端口扫描
    '''
    return new_task('nmap',options)


@celery_app.task(base=UpdateTaskStatus)
def iplocation( options):
    '''获取ip的归属地
    '''
    return new_task('iplocation',options)


@celery_app.task(base=UpdateTaskStatus)
def webtitle(options):
    '''获取title
    '''
    return new_task('webtitle',options)


@celery_app.task(base=UpdateTaskStatus)
def domainip( options):
    '''查询域名IP
    '''
    return new_task('domain',options)


@celery_app.task(base=UpdateTaskStatus)
def portscan(options):
    '''端口扫描综合任务
    '''
    return new_task('portscan',options)


@celery_app.task(base=UpdateTaskStatus)
def fofasearch(options):
    '''调用fofa API
    '''
    return new_task('fofasearch',options)


@celery_app.task(base=UpdateTaskStatus)
def subdomain(options):
    '''调用Sublist3r收集子域名信息
    '''
    return new_task('submain',options)

@celery_app.task(base=UpdateTaskStatus)
def domainscan(options):
    '''域名收集综合信息
    '''
    return new_task('domainscan',options)
