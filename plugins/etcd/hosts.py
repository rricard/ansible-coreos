#!/usr/bin/env python

import os
import etcd
import json


def last_key_element(key):
    return key.split('/')[-1]

master = json.loads(
    os.getenv('ETCD_MASTER', '{"ansible_ssh_host":"127.0.0.1"}')
)
host = os.getenv('ETCD_HOST', master['ansible_ssh_host'])
port = os.getenv('ETCD_PORT', 4001)
ssh_host = os.getenv('SSH_HOST', host)
ssh_port = os.getenv('SSH_PORT', 22)
namespace = os.getenv('ETCD_NAMESPACE', 'ansible')

client = etcd.Client(host=host, port=port)

output = {
    '_meta': {
        'hostvars': {
            'etcd_master': master
        }
    }
}

try:
    groups = client.node.get('/%s/groups' % (namespace), recursive=True)

    for group in groups.node.children:
        group_name = last_key_element(group.key)
        if group.is_directory:
            output[group_name] = {'hosts': []}
            for host in group.children:
                host_name = last_key_element(host.key)
                output['_meta']['hostvars'][host_name] = json.loads(host.value)
                output[group_name]['hosts'].append(host_name)
        else:
            output[group_name] = json.loads(group.value)
except KeyError:
    pass

print json.dumps(output)
