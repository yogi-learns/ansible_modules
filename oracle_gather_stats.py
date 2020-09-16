#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Yogi
# GNU General Public Licence v3.0+
# https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oracle_gather_stats
short_description: Gather database statistics
description:
    - Gather database statistics for given database
    - Makes a remote connection to target database
version_added: "2.9.10"
author: Yogesh Tiwari (@yogiboy)
options:
    hostname:
        description:
            - Provide the database hostname
        required: False
        default: localhost
    db_port:
        description:
            - Provide port number for database
        required: False
        default: 1521
    service_name:
        description:
            - Provide service name for database
        required: True
    user:
        description:
            - Provide username to use for connection
        required: True
        default: sys
    password:
        description:
            - Provide password to use for connection
        required: True
    mode:
        description:
            - Choose type of connection
        required: True
        default: normal
        choices: ['normal','sysdba']
notes:
    - uses python cx_oracle module for remote connection
requirements: ['cx_oracle']
'''

EXAMPLES = '''
- name: Gather Database stats
  oracle_gather_stats:
    hostname: localhost
    db_port: 1521
    service_name: ORCLPDB1
    user: sys
    password: K2ypton55
    mode: sysdba
'''

from ansible.module_utils.basic import AnsibleModule
from datetime import timedelta

try:
    import cx_Oracle
except ImportError:
    cx_oracle_exists = False
else:
    cx_oracle_exists = True

def gather_stats_func():
    c = connection.cursor()
    c.callproc('dbms_stats.gather_database_stats')
    
def main():
    global connection, msg, module
    msg = ['']
    module_args = dict(
            hostname    = dict(default='localhost'),
            db_port     = dict(default=1521, type='int'),
            service_name= dict(required=True),
            user        = dict(required=True),
            password    = dict(required=True),
            mode        = dict(default='normal', choices=['normal','sysdba'])
        )
    
#    result = dict(
#        changed=False,
#        original_message='',
#        message=''
#    )
    
    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = True
    )
    
#    if module.check_mode:
#        module.exit_json(**result)
        
#    result['original_message'] = module.params['name']
#    result['message'] = 'goodbye'

    if not cx_oracle_exists:
        module.fail_json(msg="The cx_oracle module is required. Use 'pip install cx_oracle' to install and set ORACLE_HOME & LD_LIBRARY_PATH")

    hostname    = module.params["hostname"]
    db_port     = module.params["db_port"]
    service_name= module.params["service_name"]
    user        = module.params["user"]
    password    = module.params["password"]
    mode        = module.params["mode"]
    
    try:
        if (user and password and service_name):
            if mode == 'sysdba':
                dsn =  cx_Oracle.makedsn(host=hostname, port=db_port, service_name=service_name)
                connect = dsn
                connection = cx_Oracle.connect(user, password, dsn, mode=cx_Oracle.SYSDBA)
            else:
                dsn =  cx_Oracle.makedsn(host=hostname, port=db_port, service_name=service_name)
                connect = dsn
                connection = cx_Oracle.connect(user, password, dsn)
        elif (not(user) or not(password) or not(service_name)):
            module.fail_jsaon(msg='Missing username or password or service_name for cx_Oracle')
            
    except cx_Oracle.DatabaseErrors as exc:
        error, = exc.args
        msg[0] = 'Could not connect to database - %s, connect descriptor: %s' % (error.message, connect)
        module.fail_json(msg=msg[0], changed=False)
    
    if module.check_mode:
        module.exit_json(changed=False)

    gather_stats_func()    

    connection.commit()
    module.exit_json(msg=msg, changed=True)

if __name__ == '__main__':
    main()

