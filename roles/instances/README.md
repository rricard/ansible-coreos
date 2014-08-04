instances
=========

Creates instances of a docker container running the same image and launch them with fleet.

Requirements
------------

Runs out of the on CoreOS.

Role Variables
--------------

| Name         | Default             | Description                                   |
|--------------|---------------------|-----------------------------------------------|
| name         | `service`           | The service's name which will be run by fleet |
| image        | `phusion/baseimage` | The image running inside docker               |
| namespace    | `development`       | The etcd base path to register the instances  |
| conflicts    | `True`              | Prevent similar instances from spawning on the same server |
| persists     | `False`             | Try to persists the container state in case of shutdown (deprecated) |
| instances    | `service.0`         | The list of the anstance's names              |

Example
-------

```
- name: Setup the node.js containers
  hosts: master
  roles:
  - role: instances
    name: nodeapp
    image: custom/nodeapp
    instances:
    - node.0
    - node.1
    - node.2
```

Dependencies
------------

There's no ansible dependencies needed.

License
-------

MIT

Author
------

[Robin Ricard](https://github.com/rricard/)
