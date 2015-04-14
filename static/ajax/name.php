<?php
if(isset($_POST['name'])==true && empty($_POST['name'])==false){
	require '../db/connect.php';

	$query= mysql_query("SELECT 'names'.'location' from 'names' where 'names'.'name'='".mysql_real_escape_string(trim($_POST['name']))."'");
	echo  (mysql_num_rows($query)!=0)?mysql_result($query,0,'location'):'Name not found';
}
?>