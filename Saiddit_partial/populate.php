<?php
	//Start session
	session_start();	
	//Unset the variables stored in session
	unset($_SESSION['SESS_MEMBER_ID']);
	unset($_SESSION['SESS_USERNAME']);
	unset($_SESSION['SESS_REPUTATION']);
?>
<tr>
    <p align="left"><a href="front.php">Go back</a></p>
  </tr>

<form name="loginform" action="insert.php" method="post" action="connection.php">
<table height ="300" width="309" border="0" align="center" cellpadding="2" cellspacing="5">
<body background = "img.jpg" no-repeat;>
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
    <td width="116"><div align="right"><p><font color="#38610B"><b><big>Mary</big></b></font></p></div></td>
  </tr>
  
  <tr>
    <td width="116"><div align="right">Title</div></td>
    <td width="177"><input name="title" type="text" size ="40"/></td>
  </tr>
  <tr>
    <td><div align="right">Text</div></td>
    <td><input name="text" type="text" size ="40" style="height:300px;"/></td>
   <tr>
    <td width="116"><div align="right">Url</div></td>
    <td width="177"><input name="url" type="text" size ="40"/></td>
  </tr>
  <tr>
    <td><div align="right"></div></td>
    <td><input name="" type="submit" value="Make Posts" /></td>
  </tr>
</table>
</form>
