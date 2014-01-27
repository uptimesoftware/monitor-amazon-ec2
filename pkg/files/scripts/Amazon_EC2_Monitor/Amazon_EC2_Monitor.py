#!/usr/bin/python

import sys
import os
import boto
import datetime

from boto.exception import BotoServerError

AWS_ACCESS_KEY = os.environ.get('UPTIME_AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('UPTIME_AWS_SECRET_KEY')

# EC2 statuses
EC2_STATUS = {"running": 0, "shutting-down":1, "stopping":2, "pending":3, "terminated":4, "stopped":5}

class Error(Exception):
    pass

def main(argv):
	try:
		ec2 = boto.connect_ec2(AWS_ACCESS_KEY, AWS_SECRET_KEY)
		
		reservations = ec2.get_all_instances()
		instances = [i for r in reservations for i in r.instances]

		c = boto.connect_cloudwatch(AWS_ACCESS_KEY, AWS_SECRET_KEY)
		end = datetime.datetime.now()
		start = end - datetime.timedelta(hours=1)

		metrics = ['CPUUtilization', 'DiskReadBytes', 'DiskReadOps', 'DiskWriteBytes', 'DiskWriteOps', 'NetworkIn', 'NetworkOut']
		
		for instance in instances:
			print instance.id + ".Availability ", 
			print EC2_STATUS[instance.state]
			if instance.state == "running":		# pull stats for running instances only
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
					print instance.id + "." + metrics[j],
					print stats[len(stats)-1]['Average']	# get last reading

	except BotoServerError as serverErr:
		print json.dumps({
			"error": "Error retrieving CloudWatch metrics."
		})
		sys.exit(2)

if __name__ == "__main__":
	main(sys.argv[1:])
	sys.exit(0)