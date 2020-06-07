#!/usr/bin/env python3
# coding:utf-8
from nemo.core.database.ip import Ip
from nemo.core.database.port import Port
from nemo.core.database.domain import Domain
from nemo.core.database.organization import Organization
from nemo.core.database.attr import IpAttr, PortAttr, DomainAttr


def __get_ip_domain(ip):
    '''查询IP关联的域名
    '''
    domain_set = set()
    domain_attrs_obj = DomainAttr().gets(query={'tag': 'A', 'content': ip})
    for domain_attr_obj in domain_attrs_obj:
        domain_obj = Domain().get(domain_attr_obj['r_id'])
        if domain_attr_obj:
            domain_set.add(domain_obj['domain'])

    return domain_set

def get_ip_port_info(ip, ip_id):
    '''获取IP端口属性，并生成port、title、banner聚合信息
    '''
    port_list = []
    title_set = set()
    banner_set = set()
    ports_attr_info = []

    ports_obj = Port().gets(query={'ip_id': ip_id})
    for port_obj in ports_obj:
        port_list.append(port_obj['port'])
        # 获取端口属性
        port_attrs_obj = PortAttr().gets(query={'r_id': port_obj['id']})
        FIRST_ROW = True
        # 每个端口的一个属性生成一行记录
        # 第一行记录显示IP和PORT，其它行保持为空（方便查看）
        for port_attr_obj in port_attrs_obj:
            pai = {}
            if FIRST_ROW:
                pai.update(ip=ip, port=port_obj['port'])
                FIRST_ROW = False
            else:
                pai.update(ip='', port='')
            pai.update(tag=port_attr_obj['tag'], content=port_attr_obj['content'], source=port_attr_obj['source'],
                       update_datetime=port_attr_obj['update_datetime'].strftime('%Y-%m-%d %H-%M'))
            # 更新集合
            if port_attr_obj['tag'] == 'title':
                title_set.add(port_attr_obj['content'])
            elif port_attr_obj['tag'] in ('banner', 'tag', 'server'):
                banner_set.add(port_attr_obj['content'])

            ports_attr_info.append(pai)

    return port_list, title_set, banner_set, ports_attr_info


def get_ip_info(Id):
    '''聚合一个IP的详情
    '''
    ip_info = {}
    # 获取IP
    ip_obj = Ip().get(Id)
    if not ip_obj:
        return None
    ip_info.update(ip=ip_obj['ip'], location=ip_obj['location'], status=ip_obj['status'], update_dateime=ip_obj['update_datetime'].strftime(
        '%Y-%m-%d %H-%M'))
    # 获取组织名称
    if ip_obj['org_id']:
        organziation__obj = Organization().get(ip_obj['org_id'])
        if organziation__obj:
            ip_info.update(organiztion=organziation__obj['org_name'])
    else:
        ip_info.update(Organization='')
    # 端口、标题、banner、端口详情
    port_list, title_set, banner_set, ports_attr_info = get_ip_port_info(
        ip_obj['ip'], ip_obj['id'])
    ip_info.update(port_attr=ports_attr_info)
    ip_info.update(title=list(title_set))
    ip_info.update(banner=list(banner_set))
    ip_info.update(port=port_list)
    # IP关联的域名
    domain_set = __get_ip_domain(ip_obj['ip'])
    ip_info.update(domain=list(domain_set))

    return ip_info


def get_domain_info(Id):
    '''聚合一个DOMAIN的详情
    '''
    domain_info = {}
    # 获取DOMAIN
    domain_obj = Domain().get(Id)
    if not domain_obj:
        return None
    domain_info.update(
        domain=domain_obj['domain'], update_datetime=domain_obj['update_datetime'].strftime('%Y-%m-%d %H-%M'))
    # 获取组织名称
    if domain_obj['org_id']:
        organziation__obj = Organization().get(domain_obj['org_id'])
        if organziation__obj:
            domain_obj.update(organiztion=organziation__obj['org_name'])
    else:
        domain_obj.update(Organization='')
    domain_attrs_obj = DomainAttr().gets(query={'r_id': domain_obj['id']})
    # 获取域名的属性信息：title和ip
    title_set = set()
    ip_set = set()
    for domain_attr_obj in domain_attrs_obj:
        if domain_attr_obj['tag'] == 'title':
            title_set.add(domain_attr_obj['content'])
        elif domain_attr_obj['tag'] == 'A':
            ip_set.add(domain_attr_obj['content'])
    domain_info.update(title= list(title_set))
    # 获取域名关联的IP端口详情：
    port_set = set()
    ip_port_list = []
    for domain_ip in ip_set:
        ip_obj = Ip().gets(query={'ip': domain_ip})
        if ip_obj and len(ip_obj) > 0:
            p, _, _, pai = get_ip_port_info(ip_obj[0]['ip'], ip_obj[0]['id'])
            port_set.update(p)
            ip_port_list.extend(pai)    
    domain_info.update(ip=list(ip_set))
    domain_info.update(port=list(port_set))
    domain_info.update(ip_port_info=ip_port_list)

    return domain_info


Id = 162
ip_info = get_ip_info(Id)
for k, v in ip_info.items():
    print(k, ':', v)

Id = 911
domain_info = get_domain_info(Id)
for k, v in domain_info.items():
    print(k, ':', v)

def main():
    pass


if __name__ == '__main__':
    main()
