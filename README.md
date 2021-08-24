## Devops_work

## A Utility to collect Jenkins Last Successful Jobs Data
Purpose: To collect the last successful jenkins jobs details like executor, date, time, parameters we can fetch using this utility.

## conf.py details
You need to specify following parameters before execution of 'jenkins_jobs_details.py' script

  jenkins_url="http://<IP>:8080"
  jenkins_username="USERNAME"
  jenkins_password="PASSWORD"
  jenkins_dirname="DIRECTORY_NAME"
  jenkins_jobsubstr="SUB_STRING"
  jenkins_outputfile = "./<OUTPUT_FILE_NAME>.txt"


## To Run jenkins_jobs_details.py 
>> python3 jenkins_jobs_details.py

The script will shows you the actual output on terminal as well as it will create a <OUTPUT_FILE_NAME.txt> which stores last successful job details
The path of <OUTPUT_FILE_NAME.txt> is resides where the jenkins_jobs_details.py is present 

## OUTPUT_FILE_NAME.txt stores Last Successful Jobs data sequentially wrt Job

