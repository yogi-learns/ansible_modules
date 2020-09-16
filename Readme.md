# Ansible Modules (Custom)
This repository contains custom ansible modules that serve a specific purpose

## oracle_gather_stats
This ansible module gather database stats for given database.

### Dependency

This module needs python 3.6 or higher.

If ansible on your machine uses python 2. Install python 3 and set following in your inventory file
_example - /etc/ansible/hosts_
```
localhost ansible_host=localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3
```

### Usage

* Clone this repository and import this module

Set ANSIBLE_LIBRARY environment variable pointing to directory containing module

* Create ansible playbook task

_example_
```
## gather_db_stats.yml
---

- hosts: localhost
  vars:
    hostname: localhost
    user: sys
    password: K2ypton55
    mode: sysdba
    db_port: 1521
    service_name: orclpdb1
    oracle_env:
      ORACLE_HOME: /opt/oracle/product/19c/dbhome_1
      LD_LIBRARY_PATH: /opt/oracle/product/19c/dbhome_1/lib
  tasks:
    - name: Gather database stats in pdb orclpdb1
      oracle_gather_stats:
        hostname: "{{ hostname }}"
        user: "{{ user }}"
        password: "{{ password }}"
        mode: "{{ mode }}"
        db_port: "{{ db_port }}"
        service_name: "{{ service_name }}"
      environment: "{{ oracle_env }}"
```
* Run ansible playbook

```
ansible-playbook gather_db_stats.yml
```

