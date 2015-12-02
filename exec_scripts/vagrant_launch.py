#!/usr/bin/python3

import subprocess, sys
sys.path.append('/root/hubops')
project_dir = '/root/hubops'

def vagrant_health_checks():
    #Check for vagrant init
    current_status = subprocess.call(['{}/exec_scripts/vagrant_up.sh'.format(project_dir),'c_init'])
    if current_status == 0:
        print("Vagrant was already initialized. Proceeding now...")
    elif current_status == 1:
        print("Vagrant has been initialized. Proceeding now...")


def vagrant_box_add(provider):
    box_list = subprocess.check_output(['vagrant','box','list','--machine-readable']).decode('utf-8').split('\n')
    for box_attr in box_list:
        if box_attr.split(',')[3] == user_box_pref:
            print("The box exists locally. Proceeding now...")
            return 0
            break
        else:
            print("The box does not exist locally. Trying to pull from atlas.hashicorp.com")
            box_pull_status = subprocess.call(['{}/exec_scripts/vagrant_up.sh'.format(project_dir),'box_pull',user_box_pref,provider])
            if box_pull_status == 0:
                print("The box {} with provider {} has been added successfully!".format(user_box_pref,provider))
                return 0
            elif box_pull_status == 1:
                    print("Incorrect box name entered / Box not found on remote server. Please enter again!")
                    return 1
            elif box_pull_status == 2:
                print("TTY is required for this operation. Modify the code, sorry about that!")
                return 1
            elif box_pull_status == 3:
                print("Oh, the box already exists on the server. Using {}.".format(user_box_pref))
                return 0
            elif box_pull_status == 4:
                print("Box does not support the provider {}. Browse atlas.hashicorp.com for alternatives...".format(provider))
                return 1
            elif box_pull_status == 404:
                print("Some error has occurred, try entering the details again...")
                return 1






if __name__ == '__main__':
    vagrant_health_checks()
    provider_list = ['virtualbox']
    while True:
        global user_box_pref
        user_box_pref = input("Which box do you want to work with?\n")
        print("You can use one of these providers currently. More to be supported soon!")
        for provider_name in provider_list:
            print("Enter {} for {}.".format(provider_list.index(provider_name),provider_name))
        box_provider = provider_list[int(input())]
        if vagrant_box_add(box_provider) == 0:
            break