#!/bin/sh
inst=`grep pidfile /etc/init.d/uptime_core | head -n 1 | cut -d: -f2 | rev | cut -c 12- | rev | sed -e 's/^[ \t]*//'`
MIBDIRS=$inst/mibs
export MIBDIRS

python Amazon_EC2_Monitor.py
curdir=`pwd`
if [ "$?" = "0" ]; then
	../addsystem "$curdir/instances.txt" >> addsystem.log
	if [ "$?" = "0" ]; then
		/usr/local/uptime/apache/bin/php Amazon_EC2_Monitor_Update_Host_Check.php >> updatehostcheck.log
		if [ "$?" != "0" ]; then
			echo "Error - Amazon_EC2_Monitor_Update_Host_Check.php: " 1>&2
			exit 2
		fi
	else
		echo "Error - addsystem: " 1>&2
		exit 2
	fi
else
	echo "Error - Amazon_EC2_Monitor.py: " 1>&2
	exit 2
fi
