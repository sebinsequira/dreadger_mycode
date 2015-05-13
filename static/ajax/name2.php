<?php 
    $hostname_connection = "localhost"; 
    $database_connection = "dreadger"; 
    $username_connection = "admin"; 
    $password_connection = "aaggss"; 
    $connection = mysql_connect($hostname_connection, $username_connection, $password_connection) or trigger_error(mysql_error(),E_USER_ERROR); 
    mysql_select_db($database_connection,$connection) or die( mysql_error("could not connect to database! " ) ) ; 
?>

<?php $display ="select * from db order by time desc limit 1"; 
    $result=mysql_query($display,$connection) or die(mysql_error()); 
    if($result == FALSE) 
      { die(mysql_error()); }
?>

<?php 
    $rows = mysql_fetch_assoc($result);
    $return_data=array('time' => $rows['time'],
        'storage_tank_level'  => $rows['storage_tank_level'],
        'storage_tank_cap'    => $rows['storage_tank_cap'],
        'service_tank_level'  => $rows['service_tank_level'],
        'service_tank_cap'    => $rows['service_tank_cap'],
        'flowmeter_1_in'      => $rows['flowmeter_1_in'],
        'flowmeter_1_out'     => $rows['flowmeter_1_out'],
        'engine_1_status'     => $rows['engine_1_status'],
        'flowmeter_2_in'      => $rows['flowmeter_2_in'],
        'flowmeter_2_out'     => $rows['flowmeter_2_out'],
        'engine_2_status'     => $rows['engine_2_status']);
    header('Content-Type: application/json');
    echo json_encode($return_data);
    exit();
  ?>


