#!/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import config
import tabulate
import datetime
import os.path
from datetime import datetime

## configuration data from config.py file
JENKINS_URL = config.jenkins_url
JENKINS_USERNAME = config.jenkins_username
JENKINS_PASSWORD = config.jenkins_password
JENKINS_DIRNAME = config.jenkins_dirname
JENKINS_JOBNAME = config.jenkins_jobname
JENKINS_JOBS_SUBSTR = config.jenkins_jobsubstr
JENKINS_OUTPUTFILE = config.jenkins_outputfile

from jenkinsapi.jenkins import Jenkins

def get_server_instance():
    jenkins_url = JENKINS_URL
    server = Jenkins(jenkins_url, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
    return server
print (get_server_instance())

def get_job_details():
    server = get_server_instance()

    for job_name, job_instance in server.get_jobs():
        all_job_name_list=job_instance.name
        # print('all job: ' + str(all_job_name_list))
        if not (not (JENKINS_JOBS_SUBSTR is not None) or not (JENKINS_JOBS_SUBSTR in all_job_name_list)):
            # print('Job Name: '+str(all_job_name_list))
            base_url = ('%(u)s/job/%(d)s/job/%(j)s' % {'u': JENKINS_URL, 'd': JENKINS_DIRNAME, 'j': all_job_name_list})
            username = JENKINS_USERNAME
            password = JENKINS_PASSWORD
            url = (base_url + '/api/json')
            #print('\nBase_url :' + str(base_url))
            response = requests.get(url, auth=(username, password), verify=False)
            ##print(str(response))
            ## File operations

            f = open(JENKINS_OUTPUTFILE, 'a+')
            try:
                buildnumberJson = json.loads(response.text)
            except:
                print("Failed to parse json")

            if "lastBuild" in buildnumberJson:
                totalbuilds = buildnumberJson["lastBuild"]
                runs = totalbuilds["number"]
            else:
                print("Failed to get build")

            # Iterate over the job build runs to get the build status for each
            lastSuccessfulBuildurl = (base_url + '/lastSuccessfulBuild/api/json')
            last_success_job_data = []
            print('Last Successful Build Json: ' + str(lastSuccessfulBuildurl))
            print('Job Name: ' + str(all_job_name_list))
            f.write('\nLast Successful Build Json: ' + str(lastSuccessfulBuildurl))
            f.write('\nJob Name: ' + str(all_job_name_list))

            try:
                response = requests.get(lastSuccessfulBuildurl, auth=(username, password), verify=False)
                last_success_job_data = json.loads(response.text)
                result = last_success_job_data['result']
                #print('Last Build Result: ' + str(result))

            except Exception as e:
                print(str(e))
            if "result" in last_success_job_data:
                if last_success_job_data["result"] == "SUCCESS":
                    result = last_success_job_data['result']
                    build_no = last_success_job_data['id']
                    executor = last_success_job_data['executor']
                    full_disp_name = last_success_job_data['fullDisplayName']
                    date = last_success_job_data['timestamp']
                    timestamp = date
                    date = datetime.fromtimestamp(timestamp / 1e3)
                    
                    print('Job FullName: ' + str(full_disp_name))
                    print('Job Result: ' + str(result))
                    print('Executor Name: ' + str(executor))
                    print('Last Successful Build No: ' + str(build_no))
                    print('Date: ' + str(date))
                    
                    f.write('\nJob FullName: ' + str(full_disp_name)+'\n')
                    f.write('Job Result: ' + str(result)+'\n')
                    f.write('Executor Name: ' + str(executor)+'\n')
                    f.write('Last Successful Build No: ' + str(build_no)+'\n')
                    f.write('Date: ' + str(date)+'\n')
                    # if get_all_param != 'NULL':
                    #     print('\nParameters are as belows')
                    #     header = key_value[0].keys()
                    #     rows = [x.values() for x in key_value]
                    #     print(tabulate.tabulate(rows, header))
                    #     print('--------------------****----------------------\n')
                    # elif get_all_param == 'NULL':
                    #     print('Parameters not found')
                    #     print('--------------------****----------------------')
                    if (int(build_no) <= 1):
                        get_all_param = last_success_job_data['actions'][0]
                        get_param = [dict(class_name=k1["_class"], name=k1["name"], value=k1["value"]) for k1 in get_all_param]
                        key_value = [dict(name=k1["name"], value=k1["value"]) for k1 in get_param]
                        print('\nParameters are as belows')
                        f.write('Parameters are as belows\n')
                        header = key_value[0].keys()
                        rows = [x.values() for x in key_value]
                        print(tabulate.tabulate(rows, header))
                        f.write('\n' + str(tabulate.tabulate(rows, header)))
                        print('--------------------****----------------------\n')
                        f.write('\n-----------------****--------------------')
                        f = f.close(JENKINS_OUTPUTFILE)
                    elif(int(build_no) > 2):
                        get_all_param = last_success_job_data['actions'][0]['parameters']
                        get_param = [dict(class_name=k1["_class"], name=k1["name"], value=k1["value"]) for k1 in get_all_param]
                        key_value = [dict(name=k1["name"], value=k1["value"]) for k1 in get_param]
                        key_value = [dict(name=k1["name"], value=k1["value"]) for k1 in get_param]
                        print('\nParameters are as belows')
                        f.write('\nParameters are as belows')
                        header = key_value[0].keys()
                        rows = [x.values() for x in key_value]
                        print(tabulate.tabulate(rows, header))
                        f.write('\n'+str(tabulate.tabulate(rows, header)))
                        print('--------------------****----------------------\n')
                        f.write('\n------------------------------------------')

                    else:
                        print('Job is not executed so far')
                        f.write('\nJob is not executed so far')
                        f = f.close(JENKINS_OUTPUTFILE)
                if last_success_job_data["result"] == "FAILURE":
                    print('Last Build Result Is Failed')
                    f.write('\nLast Build Result Is Failed')
                    f = f.close(JENKINS_OUTPUTFILE)

print (get_job_details())
## Write Data into the file
print ('Done...')
