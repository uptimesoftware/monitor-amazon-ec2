<?php
set_time_limit(0);
header( 'Content-type: text/html; charset=utf-8' );

//set MySQL DB connection details if not the uptime defaults.
$hostname = "localhost:3308";
$dbname = "uptime";
$username = "uptime";
$pw = "uptime";
$db = mysqli_connect($hostname, $dbname, $username, $pw);
$count = 0;

if (mysqli_connect_errno()) 
{
	printf("Connection failed: %s</br>", mysqli_connect_error());
	exit();
}

$sql = "SELECT * FROM erdc_instance WHERE name LIKE 'EC2 Instance Monitor (member)' and is_host_check=0";			
$result = mysqli_query($db, $sql);
if (!$result)
{
	die('Invalid select query: ' . mysqli_error());
}

echo date('Y-m-d H:i:s') . " - " . "Start Update Host Checks\n";

while($row = mysqli_fetch_array($result))
{
	echo date('Y-m-d H:i:s') . " - " . $row['erdc_instance_id'] . " " . $row['entity_id'];
	echo "\n";
	$count++;
}

$sql = "UPDATE erdc_instance SET is_host_check=1 WHERE name LIKE 'EC2 Instance Monitor (member)'";			
$result = mysqli_query($db, $sql);
if (!$result)
{
	die('Invalid select query: ' . mysqli_error());
}

echo date('Y-m-d H:i:s') . " - " . "Update Count: " . $count . "\n";
echo date('Y-m-d H:i:s') . " - " . "End Update Host Checks"
?>