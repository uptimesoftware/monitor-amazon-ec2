#!/usr/bin/python

import sys
import os
import boto

from boto.exception import BotoServerError

AWS_ACCESS_KEY = os.environ.get('UPTIME_AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('UPTIME_AWS_SECRET_KEY')
UPTIME_GROUP = os.environ.get('UPTIME_ELEMENT_GROUP')

class Error(Exception):
    pass

def main(argv):
	try:
		ec2 = boto.connect_ec2(AWS_ACCESS_KEY, AWS_SECRET_KEY)		
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