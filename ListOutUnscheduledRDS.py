import sys
import boto3
from botocore.exceptions import ClientError
import os
import requests
import json
from os import listdir
from os.path import isfile, join


'''


 This script compares list of RDS's scheduled in the local/GIT file with the list of list of AWS RDS.


'''



def listAllAWSDBs(client):
    dbinstances = []
    response = client.describe_db_instances(
    )
    for dbinstance in response['DBInstances']:
        dbinstances.append(dbinstance['DBInstanceIdentifier'])
    
    return dbinstances



        
    
###########
#         #
#         #
#  Main   #
#         #
#         #
########### 


if __name__=='__main__':

    # Create the AWS session
    session = boto3.Session()
    
	# make sure your AWS account profile in your local machine (under aws cli folder)
    if account not in session.available_profiles:
        print("Account: " + account + " does not exist on this machine")
        sys.exit()
    else:
        # if true, building boto3 session for the customer
        session = boto3.Session(profile_name=account)


    # connecting to rds client
    rdsclient = session.client('rds')

    # list of rds in AWS
    rdslist = listAllAWSDBs(rdsclient)

    print("AWS LIST  DB " + str(rdslist))

    # Going to check the rds files in GIT/Local 
    schedulerdslist = []
    
	
	# file_path --> folder path to local file to cross check unscheduled RDS
	
	
    for eachFile in listdir(file_path):
        schedulerdslist.append(eachFile)
   
    print("SCHEDLIST DB " + str(schedulerdslist))
    
    # Checking for Unscheduled RDS
    duplicate_schedulerdslist = schedulerdslist.copy()

	a = list()
	b = list()

    for eachDb in rdslist:
        if eachDb not in duplicate_schedulerdslist:
            print("Unscheduled RDS {0}".format(eachDb))
			a.append(eachDb)
        else:
            duplicate_schedulerdslist.remove(eachDb)

    # RDS Names in folder but not present in AWS anymore.
    if len(duplicate_schedulerdslist) != 0:
        
        for eachDb in duplicate_schedulerdslist:
            print("Unscheduled RDS {0}".format(eachDb))
			b.append(eachDb)
       
	   
	print("Database defined but not found in AWS = {0}".format(a))
	print("Database found in AWS but not defined = {0}".format(b))