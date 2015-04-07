<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="3">
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="table.css">
    <?php 
    $hostname_connection = "localhost"; 
    $database_connection = "dreadger"; 
    $username_connection = "admin"; 
    $password_connection = "aaggss"; 
    $connection = mysql_connect($hostname_connection, $username_connection, $password_connection) or trigger_error(mysql_error(),E_USER_ERROR); 
    mysql_select_db($database_connection,$connection) or die( mysql_error("could not connect to database! " ) ) ; 
    ?>
  </head>

  <body>
    
    <?php $display ="select * from dieselLevel order by mTime desc limit 1"; 
    $result=mysql_query($display,$connection) or die(mysql_error()); 
    if($result == FALSE) 
      { die(mysql_error()); }
    ?>

    <div class="container">
                             
      <table class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>mTime</th>
            <th>IP</th>
          </tr>
        </thead>
        <tbody>

          <?php while($rows = mysql_fetch_assoc($result)){ ?>
            <tr>
              <td><?php echo 1?></td>
              <td><?php echo $rows['mTime'] ?></td> 
              <td><?php echo $rows['level'] ?></td> 
            </tr> 
          <?php } ?>

        </tbody>
      </table>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
  </body>

</html>
