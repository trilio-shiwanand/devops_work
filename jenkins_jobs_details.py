#!/bin/python
# -*- coding: utf-8 -*-
import csv

import requests
import json
import config
import datetime
import re
import pandas as pd
from datetime import datetime

## configuration data from config.py file
JENKINS_URL = config.jenkins_url
JENKINS_USERNAME = config.jenkins_username
JENKINS_PASSWORD = config.jenkins_password
JENKINS_DIRNAME = config.jenkins_dirname
JENKINS_JOBS_SUBSTR = config.jenkins_jobsubstr
JENKINS_OUTPUTFILE = config.jenkins_outputfile
JENKINS_REPORTFILE = config.jenkins_last_successful_jobs_report

from jenkinsapi.jenkins import Jenkins

def get_server_instance():
    jenkins_url = JENKINS_URL
    server = Jenkins(jenkins_url, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
    return server
print (get_server_instance())

def get_job_details():
    server = get_server_instance()
    # adding header
    headerList = ['JOB_NAME', 'BUILD_NO', 'DATE_TIME', 'RUN_USER', 'LAUNCH_NEW_OPENSTACK', 'LAUNCH_NEW_TVM', 'MASTER_CONFIG','GIT_BRANCH_NAME', 'TVAULTBUILD_NUMBER', 'NOVA_BACKEND', 'STORAGES', 'UPGRADE_BUILD', 'UPGRADE_FURY_REPO', 'UPGRADE_VERSION', 'UPGRADE_CFG_BRANCH', 'DOCKER_SOURCE']
    headerList = (str(headerList))
    headerList = re.findall(r"'(.*?)'", headerList, re.DOTALL)
    headerList = str(headerList)[1:-1]

    headerList = headerList.strip('"')
    headerList = headerList.replace("'", "")

    f = open(JENKINS_OUTPUTFILE, 'w')
    f.write(headerList)
    f.write('\n')

    for job_name, job_instance in server.get_jobs():
        all_job_name_list=job_instance.name
        f = open(JENKINS_OUTPUTFILE, 'a+')

        if not (not (JENKINS_JOBS_SUBSTR is not None) or not (JENKINS_JOBS_SUBSTR in all_job_name_list)):
            base_url = ('%(u)s/job/%(d)s/job/%(j)s' % {'u': JENKINS_URL, 'd': JENKINS_DIRNAME, 'j': all_job_name_list})
            username = JENKINS_USERNAME
            password = JENKINS_PASSWORD
            url = (base_url + '/api/json')
            response = requests.get(url, auth=(username, password), verify=False)


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
            print('JOB_NAME: ' + str(all_job_name_list))

            try:
                response = requests.get(lastSuccessfulBuildurl, auth=(username, password), verify=False)
                last_success_job_data = json.loads(response.text)
                result = last_success_job_data['result']
            except Exception as e:
                print(str(e))

            if "result" in last_success_job_data:

                if last_success_job_data["result"] == "SUCCESS":
                    result = last_success_job_data['result']
                    build_no = last_success_job_data['id']
                    executor = last_success_job_data['executor']
                    date = last_success_job_data['timestamp']
                    timestamp = date
                    date = datetime.fromtimestamp(timestamp / 1e3)
                    # full_disp_name = last_success_job_data['fullDisplayName']

                    ## Print on Terminal
                    print('RESULT: ' + str(result))
                    print('USERNAME: ' + str(executor))
                    print('BUILD_NO: ' + str(build_no))
                    print('DATE_TIME: ' + str(date))

                    ##Hardocded csv header

                    ## Write Data into csv
                    one_job_data = (str(all_job_name_list), str(build_no), str(date), str(executor) + ',')
                    one_job_data = str(one_job_data)[1:-1]

                    if (int(build_no) <= 1):
                        get_all_param = last_success_job_data['property'][2]['parameterDefinitions']
                        get_param = [dict(class_name=k1["_class"], name=k1["name"], value=k1["value"]) for k1 in get_all_param]
                        key_value = [dict(value=k1["value"]) for k1 in get_param]
                        # header = key_value[0].keys()

                        rows = [x.values() for x in key_value]
                        final_rows = (str(rows))
                        final_rows = re.findall(r"'(.*?)'", final_rows, re.DOTALL)
                        final_rows = str(final_rows)[1:-1]

                        print('\nParameters are as belows')
                        record = (str(one_job_data) + str(final_rows))

                        ## Remove Single and double quotes
                        record = record.strip('"')
                        record = record.replace("'", "")
                        print(record)

                        f.write(record)
                        f.write('\n')
                        print('--------------------****----------------------\n')

                    elif(int(build_no) > 1):
                        get_all_param = last_success_job_data['actions'][0]['parameters']
                        get_param = [dict(class_name=k1["_class"], name=k1["name"], value=k1["value"]) for k1 in get_all_param]
                        key_value = [dict(value=k1["value"]) for k1 in get_param]
                        # header = key_value[0].keys()

                        rows = [x.values() for x in key_value]
                        final_rows = (str(rows))
                        final_rows = re.findall(r"'(.*?)'", final_rows, re.DOTALL)
                        final_rows = str(final_rows)[1:-1]

                        print('\nParameters are as belows')
                        record = (str(one_job_data) + str(final_rows))

                        ## Remove Single and double quotes
                        record = record.strip('"')
                        record = record.replace("'", "")
                        print(record)

                        f.write(record)
                        f.write('\n')
                        print('--------------------****----------------------\n')

                    else:
                        print('Job is not executed so far')
                        f.write('\nJob is not executed so far')
                        f = f.close(JENKINS_OUTPUTFILE)
                if last_success_job_data["result"] == "FAILURE":
                    print('Last Build Result Is Failed')
                    f.write('\nLast Build Result Is Failed')
                    f = f.close(JENKINS_OUTPUTFILE)
get_job_details()

def csv_to_html():
    a = pd.read_csv(JENKINS_OUTPUTFILE)
    print(a)
    a.to_html(JENKINS_REPORTFILE)
    html_file = a.to_html()
csv_to_html()


print ('Done...')
