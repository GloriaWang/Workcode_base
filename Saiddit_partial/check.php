<?php
$username = "root";
$password = "123";
$hostname = "127.0.0.1"; 

//connection to the database
$dbhandle = mysql_connect($hostname, $username, $password) 
  or die("Unable to connect to MySQL");
echo "Connected to MySQL<br>";
?>
