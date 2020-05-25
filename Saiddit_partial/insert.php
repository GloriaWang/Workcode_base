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
	$title = clean($_POST['title']);
	$text = clean($_POST['text']);
	$url = clean($_POST['url']);
 
	//Input Validations
	if($title == '') {
		$errmsg_arr[] = 'Title missing';
		$errflag = true;
	}
	if($text == '') {
		$errmsg_arr[] = 'text missing';
		$errflag = true;
	}
	if($url == '') {
		$errmsg_arr[] = 'url missing';
		$errflag = true;
	}
 
	//If there are input validations, redirect back to the login form
	if($errflag) {
		$_SESSION['ERRMSG_ARR'] = $errmsg_arr;
		session_write_close();
		header("location: populate.php");
		exit();
	}
 
	//Create query
	$qry="INSERT INTO Posts(Title, Url, Text, Upvotes, Downvotes, Creator) VALUES('$title', '$url', '$text', '0', '0', 'Mary')";
	$result=mysql_query($qry);
 
	//Check whether the query was successful or not
	if($result) {
		header("location: front.php");
	}else {
		die("Query failed");
	}
	
?>