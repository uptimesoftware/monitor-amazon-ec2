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

$sql = "SELECT erdc_instance.erdc_instance_id, erdc_instance.name, entity.entity_id, entity.display_name FROM erdc_instance INNER JOIN entity ON erdc_instance.entity_id=entity.entity_id WHERE erdc_instance.name LIKE 'EC2 Instance Performance Monitor (member)' and erdc_instance.is_host_check=0";			
$result = mysqli_query($db, $sql);
if (!$result)
{
	die('Invalid select query: ' . mysqli_error());
}

echo date('Y-m-d H:i:s') . " - " . "Start Update Host Checks\n";

while($row = mysqli_fetch_array($result))
{
	echo date('Y-m-d H:i:s') . " - erdc_instance_id=" . $row['erdc_instance_id'] . " name=" . $row['name'] . " entity_id=" . $row['entity_id'] . " display_name=" . $row['display_name'];
	echo "\n";
	$count++;
}

$sql = "UPDATE erdc_instance SET is_host_check=1 WHERE name LIKE 'EC2 Instance Performance Monitor (member)'";	
$result = mysqli_query($db, $sql);
if (!$result)
{
	die('Invalid select query: ' . mysqli_error());
}

echo date('Y-m-d H:i:s') . " - " . "Update Count: " . $count . "\n";
echo date('Y-m-d H:i:s') . " - " . "End Update Host Checks"
?>
