#!/bin/sh
inst=`grep pidfile /etc/init.d/uptime_core | head -n 1 | cut -d: -f2 | rev | cut -c 12- | rev | sed -e 's/^[ \t]*//'`
MIBDIRS=$inst/mibs
export MIBDIRS

python monitor-amazon-ec2.py
curdir=`pwd`
if [ "$?" = "0" ]; then
	../../../scripts/addsystem "$curdir/instances.txt" >> addsystem.log
	if [ "$?" = "0" ]; then
		/usr/local/uptime/apache/bin/php monitor-amazon-ec2-update-host-check.php >> updatehostcheck.log
		if [ "$?" != "0" ]; then
			echo "Error - monitor-amazon-ec2-update-host-check.php: " 1>&2
			exit 2
		fi
	else
		echo "Error - addsystem: " 1>&2
		exit 2
	fi
else
	echo "Error - monitor-amazon-ec2.py: " 1>&2
	exit 2
fi
