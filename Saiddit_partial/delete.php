
<tr>
    <p align="left"><a href="front.php">Go back</a></p>
  </tr>
<form name="loginform" action="delete_exec.php" method="post" action="connection.php">
<table height ="100" width="309" border="0" align="center" cellpadding="2" cellspacing="5">
<body background = "img.jpg" no-repeat;>
  <tr>
    <td width="116"><div align="left">Input the number that you want to delete</div></td>
    <td width="177"><input name="ID" type="text" size ="10"/></td>
  </tr>
  <tr>
    <td><div align="right"></div></td>
    <td><input name="" type="submit" value="Delete" /></td>
  </tr>
</table>
</form>
<?php
	//Start session
	session_start();	
	//Unset the variables stored in session
	unset($_SESSION['SESS_MEMBER_ID']);
	unset($_SESSION['SESS_USERNAME']);
	unset($_SESSION['SESS_REPUTATION']);
	$connection = mysql_connect('127.0.0.1', 'root', '123'); //The Blank string is the password
	mysql_select_db('Saiddit');

	$query = "SELECT * FROM Posts WHERE Creator='Mary' ORDER BY Upvotes DESC;"; //You don't need a ; like you do in SQL
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