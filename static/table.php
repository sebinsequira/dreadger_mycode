<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<htmlxmlns="http://www.w3.org/1999/xhtml"> 

<head> 
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
 	<meta http-equiv="refresh" content="3">
	<?php $hostname_connection = "localhost"; $database_connection = "dreadger"; $username_connection = "root"; $password_connection = "aaggss"; $connection = mysql_connect($hostname_connection, $username_connection, $password_connection) or trigger_error(mysql_error(),E_USER_ERROR); mysql_select_db($database_connection,$connection) or die( mysql_error("could not connect to database! " ) ) ; ?>

 </head>

<body> 

	<?php $display ="select * from dieselLevel order by mTime desc limit 1"; 
	$result=mysql_query($display,$connection) or die(mysql_error()); 
	if($result == FALSE) 
		{ die(mysql_error()); }
	?>

	<table width = "245" border="0" align = "center">
			<?php while($rows = mysql_fetch_assoc($result)){ ?>
			<tr> <td><?php echo $rows['mTime'] ?></td> 
			 <td><?php echo $rows['level'] ?></td> </tr> 
			<?php } ?>
			

	</table>
</body>
</html>



