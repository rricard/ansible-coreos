#!/usr/bin/env python

import os
import etcd
import json
import yaml


def last_key_element(key):
    return key.split('/')[-1]

master_file = open(os.getenv('MASTER_CFG', './master.yml'))
master = yaml.safe_load(master_file)
master_file.close()

client = etcd.Client(host=master['etcd_host'], port=master['etcd_port'])

output = {
    '_meta': {
        'hostvars': {
            'master': master
        }
    },
    'coreos': {
        'hosts': [
            'master'
        ]
    }
}

try:
    groups = client.node.get(
        '/%s/groups' % (master['namespace']),
        recursive=True
    )

    for group in groups.node.children:
        group_name = last_key_element(group.key)
        if group.is_directory:
            if group.is_collection:
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
