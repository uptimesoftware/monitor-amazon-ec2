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
		chain = itertools.chain.from_iterable
		existing_instances = list(chain([res.instances for res in ec2.get_all_instances()]))

		# each item in existing_instances is of type Instance, covert to string
		existing_instances = ', '.join(map(str, existing_instances))
		
		# split into instance ids 
		existing_instances = existing_instances.split("Instance:")
		
		# first item is empty, so remove it
		if '' in existing_instances: existing_instances.remove('')
		
		#cleaning up instance list of trailing commas
		for i in range(len(existing_instances)):
			temp = existing_instances[i].split(",")
			existing_instances[i] = temp[0]

		c = boto.connect_cloudwatch(AWS_ACCESS_KEY, AWS_SECRET_KEY)
		end   = datetime.datetime.now()
		start = end - datetime.timedelta(hours=1)

		metrics = ['CPUUtilization', 'DiskReadBytes', 'DiskReadOps', 'DiskWriteBytes', 'DiskWriteOps', 'NetworkIn', 'NetworkOut']

		for i in range(len(existing_instances)):

			for j in range(len(metrics)):
				stats = c.get_metric_statistics(
    				60, 
					start, 
					end, 
					metrics[j], 
					'AWS/EC2', 
					'Average', 
					{'InstanceId' : existing_instances[i] }
				)

				if stats:
					print existing_instances[i] + "." + metrics[j],
					print stats[len(stats)-1]['Average']
				if not stats:
					print existing_instances[i]
					break

	except BotoServerError as serverErr:
		print json.dumps({
			"error": "Error retrieving CloudWatch metrics."
		})

if __name__ == "__main__":
	main(sys.argv[1:])
