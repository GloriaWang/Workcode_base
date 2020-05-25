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
 <td width="116"><div align="center"><p><font color="#38610B"><b><big>Jerry's Comments</big></b></font></p></div></td>
  </tr>
  <body background = "img.jpg" no-repeat;>
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
    <p align="left"><a href="Friends.php">Go back</a></p>
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

	$query = "SELECT * FROM Subsaiddit WHERE Creator='Jerry'"; //You don't need a ; like you do in SQL
	$result = mysql_query($query);

	echo "<table>"; // start a table tag in the HTML
	echo "<tr>
              <td>ID</td>
              <td>Title</td>
              <td>Description</td>
              <td>Creator</td>
              <td>Created</td>
            </tr>\n";

	while($row = mysql_fetch_array($result)){   //Creates a loop to loop through results
	echo "<tr>
              <td>{$row['ID']}</td>
              <td>{$row['Title']}</td>
              <td>{$row['Description']}</td>
              <td>{$row['Creator']}</td>
              <td>{$row['Created']}</td>
            </tr>\n";
	}

	echo "</table>"; //Close the table in HTML

	mysql_close(); //Make sure to close out the database connection
?>

<tr>
 <td width="116"><div align="center"><p><font color="#38610B"><b><big>Jerry's Posts</big></b></font></p></div></td>
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

	$query = "SELECT * FROM Posts Where Creator= 'Jerry' ORDER BY Upvotes DESC;"; //You don't need a ; like you do in SQL
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

<tr>
    <td width="116"><div align="center"><p><font color="#38610B"><b><big>Jerry's Subscribed</big></b></font></p></div></td>
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

	$query = "SELECT * FROM Subscribed WHERE SubscribedBy ='Jerry' ORDER BY Upvotes DESC"; //You don't need a ; like you do in SQL
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
              <td>SubscribedBy</td>
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
              <td>{$row['SubscribedBy']}</td> 
            </tr>\n";
	}

	echo "</table>"; //Close the table in HTML

	mysql_close(); //Make sure to close out the database connection
?>