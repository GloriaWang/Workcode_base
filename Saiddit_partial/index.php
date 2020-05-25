<?php
	//Start session
	session_start();	
	//Unset the variables stored in session
	unset($_SESSION['SESS_MEMBER_ID']);
	unset($_SESSION['SESS_USERNAME']);
	unset($_SESSION['SESS_REPUTATION']);
?>
<form name="loginform" action="login_exec.php" method="post" action="connection.php">
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
    <td width="116"><div align="right"><p><font color="#38610B"><b><big>Login Page</big></b></font></p></div></td>
  </tr>
  <tr>
    <td width="116"><div align="right">Username</div></td>
    <td width="177"><input name="username" type="text" /></td>
  </tr>
  <tr>
    <td><div align="right">Password</div></td>
    <td><input name="password" type="password" /></td>
  </tr>
  <tr>
    <td><div align="right"></div></td>
    <td><input name="" type="submit" value="login" /></td>
  </tr>
</table>
</form>


<tr>
    <td width="116"><div align="center"><p><font color="#38610B"><b><big>Popular Posts</big></b></font></p></div></td>
  </tr>
<?php
	//Start session
	//session_start();	
	//Unset the variables stored in session
	unset($_SESSION['SESS_MEMBER_ID']);
	unset($_SESSION['SESS_USERNAME']);
	unset($_SESSION['SESS_REPUTATION']);
	$connection = mysql_connect('127.0.0.1', 'root', '123'); //The Blank string is the password
	mysql_select_db('Saiddit');

	$query = "SELECT * FROM Posts ORDER BY Upvotes DESC;"; //You don't need a ; like you do in SQL
	$result = mysql_query($query);

	echo "<table>"; // start a table tag in the HTML
	echo "<tr>
              <td>ID</td>
              <td>Published</td>
              <td>Edited</td>
              <td>Title</td>
              <td>Url</td>
              <td>Text</td> 
              <td>Upvotes</td> 
              <td>Downvotes</td> 
              <td>Creator</td> 
            </tr>\n";

	while($row = mysql_fetch_array($result)){   //Creates a loop to loop through results
	echo "<tr>
              <td>{$row['ID']}</td>
              <td>{$row['Published']}</td>
              <td>{$row['Edited']}</td>
              <td>{$row['Title']}</td>
              <td>{$row['Url']}</td>
              <td>{$row['Text']}</td> 
              <td>{$row['Upvotes']}</td> 
              <td>{$row['Downvotes']}</td> 
              <td>{$row['Creator']}</td> 
            </tr>\n";
	}

	echo "</table>"; //Close the table in HTML

	mysql_close(); //Make sure to close out the database connection
?>
<table border="1" style="color:green">
<tr>
　<td>Designed by:</td>
　<td>Gloria Wang</td>
　<td>Payal Chandel</td>
</tr>
</table>