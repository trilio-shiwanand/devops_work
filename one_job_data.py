#!/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import config
import tabulate

JENKINS_URL = config.jenkins_url
JENKINS_USERNAME = config.jenkins_username
JENKINS_PASSWORD = config.jenkins_password
JENKINS_DIRNAME = config.jenkins_dirname
JENKINS_JOBNAME = config.jenkins_jobname
JENKINS_JOBS_SUBSTR = config.jenkins_jobsubstr


## Your jenkins URL and credentials goes here
# url = 'http://192.168.16.188:8080/job/SHIWA-SCRIPTED-DSL/job/Canonical_ussuri_sanity/api/json'
# username = 'admin'
# password = 'ecf7f31d87b44afeac3c51f4c5a3f783'
base_url = ('%(u)s/job/%(d)s/job/%(j)s' % {'u': JENKINS_URL,'d': JENKINS_DIRNAME, 'j': JENKINS_JOBNAME})
print('Base_url:'+str(base_url))
print('')
#url = ('%(u)s/job/%(d)s/job/%(j)s/api/json' % {'u': JENKINS_URL,'d': JENKINS_DIRNAME, 'j': JENKINS_JOBNAME})
url = (base_url+'/api/json')
# print('url1: '+ url)
username = JENKINS_USERNAME
password = JENKINS_PASSWORD

response = requests.get(url, auth=(username, password), verify=False)
##print(str(response))

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
totalsuccess = totalfailure = totalmissing = 0
#lastSuccessfulBuildurl = 'http://192.168.16.188:8080/job/SHIWA-SCRIPTED-DSL/job/Canonical_ussuri_sanity/lastSuccessfulBuild/api/json'
#lastSuccessfulBuildurl = 'http://192.168.16.188:8080/job/SHIWA-SCRIPTED-DSL/job/Canonical_ussuri_sanity/lastSuccessfulBuild/api/json'

lastbuildurl = 'http://192.168.16.188:8080/job/SHIWA-SCRIPTED-DSL/job/Canonical_ussuri_sanity/' + str(runs)
lastSuccessfulBuildurl = (base_url+'/lastSuccessfulBuild/api/json')
last_success_job_data = []
print('Last_Successful_Build_URL:' +str(lastSuccessfulBuildurl))

try:
    response = requests.get(lastSuccessfulBuildurl, auth=(username, password), verify=False)
    last_success_job_data = json.loads(response.text)
    result = last_success_job_data['result']
    print('Last Build Result: ' + str(result))
    print('')


except Exception as e:
    totalmissing = totalmissing + 1
if "result" in last_success_job_data:
    if last_success_job_data["result"] == "SUCCESS":
        totalsuccess = totalsuccess + 1
        re = last_success_job_data['result']
        build_no = last_success_job_data['id']
        executor = last_success_job_data['executor']
        full_disp_name = last_success_job_data['fullDisplayName']
        date = last_success_job_data['timestamp']
        get_param = last_success_job_data['actions'][0]['parameters']
        get_param = [dict(class_name=k1["_class"],name=k1["name"], value=k1["value"] ) for k1 in get_param]
        key_value = [dict(name=k1["name"], value=k1["value"] ) for k1 in get_param]
        # print('Parameters:' + str(get_param))
        #print('Parameters1:' + str(key_value))

        # parameters = artifacts
        # print(str(parameters))

        # print(str(last_success_job_data))
        print('Job_Full_Name: ' + str(full_disp_name))
        print('Job_Result: ' + str(re))
        print('Executor_Name: ' + str(executor))
        print('Last_Successfull_Build_No: ' + str(build_no))
        print('Date: ' + str(date))
        print('Parameters are as belows: ')
        header = key_value[0].keys()
        rows = [x.values() for x in key_value]
        print(tabulate.tabulate(rows, header))
        # print('artifacts: ' + str(artifacts))
        print('------------------------------------------')
    if last_success_job_data["result"] == "FAILURE":
        totalfailure = totalfailure + 1

# Generate Output numbers
# print(f"total builds:{runs}")
# print(f"total succeeded builds:{totalsuccess}")
# print(f"total failed builds:{totalfailure}")
# print(f"total skipped builds:{totalmissing}")
