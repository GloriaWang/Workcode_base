<?php
	//Start session
	session_start();	
	//Unset the variables stored in session
	unset($_SESSION['SESS_MEMBER_ID']);
	unset($_SESSION['SESS_USERNAME']);
	unset($_SESSION['SESS_REPUTATION']);
?>
<form name="loginform" action="login_exec.php" method="post" action="connection.php">
<table width="309" border="0" align="center" cellpadding="2" cellspacing="5">
<tr>
    <td colspan="2">
		<!--the code bellow is used to display the message of the input validation-->
		 <?php
			if( isset($_SESSION['ERRMSG_ARR']) && is_array($_SESSION['ERRMSG_ARR']) && count($_SESSION['ERRMSG_ARR']) >0 ) {
			echo '<ul class="err">';
			foreach($_SESSION['ERRMSG_ARR'] as $msg) {
				echo '<li>',$msg,'</li>'; 
				}
			echo '</ul>';
			unset($_SESSION['ERRMSG_ARR']);
			}
		?>
	</td>
  </tr>
  <tr>
    <p align="left"><a href="index.php">Logout</a></p>
  </tr>
   <tr>
    <p align="left"><a href="mypage.php">Main Page</a></p>
  </tr>
   <tr>
    <p align="left"><a href="front.php">My Page</a></p>
  </tr>
  <tr>
    <p align="left"><a href="front.php">Go back</a></p>
  </tr>
<tr>
    <td width="116"><div align="center"><p><font color="#38610B"><b><big>My Friends List</big></b></font></p></div></td>
  </tr>
  </form>
<table width="200" border="0" align="left" cellpadding="2" cellspacing="5">
<body background = "img.jpg" no-repeat;>
<tr>
    <p align="center"><a href="Bob.php">Bob</a></p>
  </tr>
  <tr>
    <p align="center"><a href="Jerry.php"> Jerry</a></p>
  </tr>
  <tr>
    <p align="center"><a href="Sarah.php">Sarah</a></p>
  </tr>