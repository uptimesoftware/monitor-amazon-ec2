#!/usr/bin/python

import sys
import os
import os.path
import boto
import boto.ec2

from boto.exception import BotoServerError

AWS_ACCESS_KEY = os.environ.get('UPTIME_AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('UPTIME_AWS_SECRET_KEY')
UPTIME_GROUP = os.environ.get('UPTIME_ELEMENT_GROUP')

class Error(Exception):
    pass

def main(argv):
	#check for config file.
	if os.path.exists("boto.config"):
		f = open('boto.config', 'r')
		
		for line in f:
			templine=line.rstrip().split("=")
			if (templine[0] == 'proxy'):
				PROXY=templine[1]
			elif (templine[0] == 'proxy_port'):
				PROXY_PORT=templine[1]
			elif (templine[0] == 'proxy_user'):
				PROXY_USER=templine[1]
			elif (templine[0] == 'proxy_pass'):
				PROXY_PASSWORD=templine[1]			
			elif (templine[0] == 'endpoint'):
				ENDPOINT=templine[1]
			elif (templine[0] == 'endpoint_name'):
				ENDPOINT_NAME=templine[1]
			elif (templine[0] == 'region'):
				REGION=templine[1]
		f.close()
	# Validate if proxy settings are set or not
	try:
		PROXY
		PROXY_PORT
		PROXY_USER
		PROXY_PASSWORD
	except NameError:
		PROXY_SET=0
	else:
		PROXY_SET=1
	
	#Set to use default region of us-east-1
	ENDPOINT_REGION=0
	
	#test to see if there was an endpoint name set if not use endpoint as a name
	try:
		ENDPOINT_NAME
	except NameError:
		ENDPOINT_NAME = "ENDPOINT"
	
	#Test for endpoint if set then update flag for later use as well as set region info for cloudwatch
	try:
		ENDPOINT
	except NameError:
		ENDPOINT_REGION=0
	else: 
		ENDPOINT_REGION=1
	
	# test for region and if set enable the 2 regions to use for EC2 and Cloudwatch. This will override endpoint if both set.
	try:
		REGION
	except NameError:
		ENDPOINT_REGION=ENDPOINT_REGION
	else:
		ENDPOINT_REGION=2
		region1 = boto.ec2.get_region(REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
	
	try:
		#Check if using a proxy for EC2 and make approiate connection type based on info provided in config
		if (PROXY_SET == 1):
			if (ENDPOINT_REGION == 0):
				ec2 = boto.connect_ec2(AWS_ACCESS_KEY, AWS_SECRET_KEY)
			elif (ENDPOINT_REGION == 1):
				ec2 = boto.connect_ec2_endpoint(ENDPOINT,AWS_ACCESS_KEY, AWS_SECRET_KEY, proxy=PROXY, proxy_port=PROXY_PORT, proxy_user=PROXY_USER, proxy_pass=PROXY_PASSWORD)
			else: 
				ec2 = boto.connect_ec2(AWS_ACCESS_KEY, AWS_SECRET_KEY, region=region1)
		else:
			if (ENDPOINT_REGION == 0):
				ec2 = boto.connect_ec2(AWS_ACCESS_KEY, AWS_SECRET_KEY)
			elif (ENDPOINT_REGION == 1):
				ec2 = boto.connect_ec2_endpoint(ENDPOINT,AWS_ACCESS_KEY, AWS_SECRET_KEY)
			else: 
				ec2 = boto.connect_ec2(AWS_ACCESS_KEY, AWS_SECRET_KEY, region=region1)
		
			reservations = ec2.get_all_instances()
			instances = [i for r in reservations for i in r.instances]
			
			if len(instances) != 0:
				f = open(os.path.join(os.path.dirname(__file__), 'instances.txt'),'w')
				
				for instance in instances:
					f.write('Host Name: ')
					f.write(instance.id)
					f.write('\nDisplay name: ')
					f.write(instance.id)
					f.write('\nType: Virtual Node')
					f.write('\nGroup: ')
					f.write(UPTIME_GROUP)
					f.write('\nPingable: false')
					f.write('\n%%\n')			
				
				f.close()
			else:
				print "Warning: No instances found."
				sys.exit(1)

	except BotoServerError as serverErr:
		print "Error: Cannot connect to EC2.  Check your credentials and/or access to ec2.amazonaws.com on port 443."
		sys.exit(2)

if __name__ == "__main__":
	main(sys.argv[1:])
	sys.exit(0)