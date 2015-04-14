<?php 
    $hostname_connection = "localhost"; 
    $database_connection = "dreadger"; 
    $username_connection = "admin"; 
    $password_connection = "aaggss"; 
    $connection = mysql_connect($hostname_connection, $username_connection, $password_connection) or trigger_error(mysql_error(),E_USER_ERROR); 
    mysql_select_db($database_connection,$connection) or die( mysql_error("could not connect to database! " ) ) ; 
?>

<?php $display ="select * from dieselLevel order by mTime desc limit 1"; 
    $result=mysql_query($display,$connection) or die(mysql_error()); 
    if($result == FALSE) 
      { die(mysql_error()); }
?>

<?php while($rows = mysql_fetch_assoc($result)){ 
    $return_data=array('sNo'=>'1','mTime'=>'2','level'=>'3');
    header('Content-Type: application/json');
    echo 123
             
 } ?>



