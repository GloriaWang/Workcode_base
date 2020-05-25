<?php

$db = mysql_connect("127.0.0.1","root","123") or die("Fail！");

if(!mysql_query("create database if not exists `user`"))

{

     echo "Fail<br>";

}else

{

     echo "Success！<br>";

}

mysql_query("use user;");

$sql ="Create TABLE if not exists `user` ("

         ." `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,"

         ." `name` VARCHAR(10) NOT NULL,"

         ." `password` VARCHAR(16) NOT NULL"

         ." )";

if(!mysql_query($sql))

{

     echo "Fail！<br>";

}else

{

     echo "Success！<br>";

}

$sql = "Insert INTO `user` ( `name`, `password`) VALUES ( 'php-fish', '123');";

if(mysql_query($sql))

echo "Insert success！<br>";

else

echo "Fail to insert！<br>";

mysql_close($db);

?>