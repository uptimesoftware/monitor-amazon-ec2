#!/usr/bin/python

import os
import sys
import boto
import itertools
import datetime

from boto.exception import BotoServerError

AWS_ACCESS_KEY = os.environ.get('UPTIME_AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('UPTIME_AWS_SECRET_KEY')

class Error(Exception):
    pass

def main(argv):
	try:
		ec2 = boto.connect_ec2(AWS_ACCESS_KEY, AWS_SECRET_KEY)
		
		reservations = ec2.get_all_instances()
		instances = [i for r in reservations for i in r.instances]

		c = boto.connect_cloudwatch(AWS_ACCESS_KEY, AWS_SECRET_KEY)
		end   = datetime.datetime.now()
		start = end - datetime.timedelta(hours=1)

		metrics = ['CPUUtilization', 'DiskReadBytes', 'DiskReadOps', 'DiskWriteBytes', 'DiskWriteOps', 'NetworkIn', 'NetworkOut']

		for instance in instances:
			for j in range(len(metrics)):
				stats = c.get_metric_statistics(
    				60, 
					start, 
					end, 
					metrics[j], 
					'AWS/EC2', 
					'Average', 
					{'InstanceId' : instance.id}
				)

				if stats:
					print instance.id + "." + metrics[j],
					print stats[len(stats)-1]['Average']
				else:
					print instance.id
					break

	except BotoServerError as serverErr:
		print json.dumps({
			"error": "Error retrieving CloudWatch metrics."
		})

if __name__ == "__main__":
	main(sys.argv[1:])