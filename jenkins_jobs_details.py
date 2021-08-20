#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import requests
import config
import jenkinsapi



JENKINS_SERVER = config.jenkins_server
JENKINS_USERNAME = config.jenkins_username
JENKINS_PASSWORD = config.jenkins_password
JENKINS_DIRNAME = config.jenkins_dirname
JENKINS_JOBNAME = config.jenkins_jobname

print(JENKINS_SERVER)
#print ('\n'JENKINS_SERVER'\nJENKINS_USERNAME\nJENKINS_PASSWORD\nJENKINS_DIRNAME\nJENKINS_JOBNAME')


# variable used for max no. of abort jobs to pick committed changes
def get_server_instance():
    jenkins_url = JENKINS_SERVER
    server = jenkins.Jenkins(jenkins_url, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
    return server



server = jenkins.Jenkins(JENKINS_SERVER, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
current_build_number = server.get_job_info(JENKINS_JOBNAME)['lastBuild']['number']
current_build_info = server.get_build_info(JENKINS_JOBNAME, current_build_number)

print(current_build_number)
print(current_build_info)


if __name__ == '__main__':
    print (get_server_instance().version)
