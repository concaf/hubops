#!/usr/bin/python3

import subprocess, sys
sys.path.append('/root/hubops')
project_dir = '/root/hubops'

def vagrant_health_checks():
    #Check for vagrant init
    current_status = subprocess.call(['{}/exec_scripts/vagrant_checks.sh'.format(project_dir),'c_init'])
    if current_status == 0:
        print("Vagrant was already initialized.")
    elif current_status == 1:
        print("Vagrant has been initialized.")


if __name__ == '__main__':
    vagrant_health_checks()