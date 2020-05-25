<?php
	//Start session
	session_start();
 
	//Include database connection details
	require_once('connection.php');
 
	//Array to store validation errors
	$errmsg_arr = array();
 
	//Validation error flag
	$errflag = false;
 
	//Function to sanitize values received from the form. Prevents SQL injection
	function clean($str) {
		$str = @trim($str);
		if(get_magic_quotes_gpc()) {
			$str = stripslashes($str);
		}
		return mysql_real_escape_string($str);
	}
 
	//Sanitize the POST values
	$ID = clean($_POST['ID']);
	
 
	//Input Validations
	if($ID == '') {
		$errmsg_arr[] = 'Number missing';
		$errflag = true;
	}
 
	//If there are input validations, redirect back to the login form
	if($errflag) {
		$_SESSION['ERRMSG_ARR'] = $errmsg_arr;
		session_write_close();
		header("location: delete.php");
		exit();
	}
 
	//Create query
	$qry="DELETE FROM Posts WHERE ID='$ID'";
	$result=mysql_query($qry);
 
	//Check whether the query was successful or not
	if($result) {
		header("location: front.php");
	}else {
		die("Query failed");
	}
?>