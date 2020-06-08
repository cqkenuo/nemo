#!/usr/bin/env python3
# coding:utf-8
from datetime import datetime

from flask import request
from flask import render_template
from flask import Blueprint
from flask import jsonify

from .authenticate import login_check
from nemo.core.database.organization import Organization
from nemo.core.database.ip import Ip
from nemo.core.database.domain import Domain
from nemo.core.tasks.taskapi import TaskAPI


task_manager = Blueprint("task_manager", __name__)


def _str2bool(v):
    return str(v).lower() in ('true', 'success', 'yes', '1')

def _format_datetime(timestamp):
    '''将timestamp时间戳格式化
    '''
    if not timestamp:
        return ''
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _format_runtime(seconds):
    '''将执行时长的秒数转换为小时、分钟和秒
    '''
    if not seconds:
        return ''
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    result = []
    if h>0:
        result.append('{}时'.format(h))
    if m>0:
        result.append('{}分'.format(m))
    if s>0:
        result.append('{}秒'.format(s))

    return ''.join(result)

@task_manager.route('/task-start-portscan', methods=['POST'])
# @login_check
def task_start_portscan_view():
    '''启动IP端口扫描任务
    '''
    taskapi = TaskAPI()
    try:
        # 获取参数
        target = request.form.get('target', default='')
        port = request.form.get('port', default='--top-ports 1000')
        org_id = request.form.get('org_id', type=int, default=None)
        rate = request.form.get('rate', type=int, default=5000)
        nmap_tech = request.form.get('nmap_tech', type=str, default='-sS')
        iplocation = request.form.get('iplocation')
        ping = request.form.get('ping')
        webtitle = request.form.get('webtitle')
        fofasearch = request.form.get('fofasearch')

        if not target or not port:
            return jsonify({'status': 'fail', 'msg': 'no target or port'})
        # 格式化tatget
        target = [x.strip() for x in target.split('\n')]
        options = {'target': target, 'port': port,
                   'org_id': org_id, 'rate': rate, 'ping': _str2bool(ping), 'tech': nmap_tech, 'iplocation': _str2bool(iplocation), 'webtitle': _str2bool(webtitle)
                   }
        result = taskapi.start_task('portscan', kwargs={'options': options})
        if _str2bool(fofasearch):
            taskapi.start_task('fofasearch', kwargs={'options': options})

        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail', 'msg': str(e)})


@task_manager.route('/task-start-domainscan', methods=['POST'])
# @login_check
def task_start_domainscan_view():
    ''' 启动域名扫描任务
    '''
    taskapi = TaskAPI()
    try:
        # 获取参数
        target = request.form.get('target', default='')
        org_id = request.form.get('org_id', type=int, default=None)
        subdomain = request.form.get('subdomain')
        webtitle = request.form.get('webtitle')
        fofasearch = request.form.get('fofasearch')
        portscan = request.form.get('portscan')

        if not target:
            return jsonify({'status': 'fail', 'msg': 'no target'})
        # 格式化tatget
        target = [x.strip() for x in target.split('\n')]
        options = {'target': target,
                   'org_id': org_id, 'subdomain': _str2bool(subdomain), 'webtitle': _str2bool(webtitle)}
        if _str2bool(portscan):
            result = taskapi.start_task(
                'domainscan_with_portscan', kwargs={'options': options})
        else:
            result = taskapi.start_task(
                'domainscan', kwargs={'options': options})

        if _str2bool(fofasearch):
            taskapi.start_task('fofasearch', kwargs={'options': options})

        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail', 'msg': str(e)})


@task_manager.route('/task-list', methods=['GET', 'POST'])
# @login_check
def task_list_view():
    '''任务列表展示
    '''
    if request.method == 'GET':
        return render_template('task-list.html')
        
    taskapi = TaskAPI()
    data = []
    try:
        draw = int(request.form.get('draw'))
        start = int(request.form.get('start'))
        length = int(request.form.get('length'))

        task_status = request.form.get('task_status')
        task_status = None if not task_status else task_status

        task_result = taskapi.get_tasks(limit=None,state=task_status)
        if task_result['status'] == 'success':
            for k, t in task_result['result'].items():
                task = {'uuid': t['uuid'], 'name': t['name'].replace('nemo.core.tasks.tasks.', '').replace('_', '-'), 
                        'state': t['state'],'args': t['args'], 'kwargs': t['kwargs'], 'result': t['result']}
                task.update(received=_format_datetime(t['received']))
                task.update(started=_format_datetime(t['started']))
                task.update(runtime=_format_runtime(t['runtime']))
                data.append(task)
        count = len(data)
        json_data = {
            'draw': draw,
            'recordsTotal': count,
            'recordsFiltered': count,
            'data': data
        }
        return jsonify(json_data)
    except Exception as e:
        print(e)
        return jsonify({'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0})


