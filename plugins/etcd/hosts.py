#!/usr/bin/env python

import os
import etcd
import json


def last_key_element(key):
    return key.split('/')[-1]


host = os.getenv('ETCD_HOST', '127.0.0.1')
port = os.getenv('ETCD_PORT', 4001)
namespace = os.getenv('ETCD_NAMESPACE', 'ansible')

client = etcd.Client(host=host, port=port)

output = {'_meta': {'hostvars': {}}}

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

print json.dumps(output)
