<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="table.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
	
	<script type="text/javascript">
		$(document).ready(function(){
			var number=10;
			var name= 'dummyNoUse';
			$.post('ajax/name2.php',{name:name},function(data){
			$('div#sNo').text(data.sNo);
			$('div#mTime').text(data.mTime);
			$('div#level').text(data.level);
			},'json');
			function redirect(num){
				number=num;
				countdown();
			}

			function countdown(){
				
				
				setTimeout(countdown,1000);
				number--;
				$('#box').html("Redirecting in "+number+" seconds.");
				if(number<=0)
				{
					var name= 'dummyNoUse';
					$.post('ajax/name2.php',{name:name},function(data){
					$('div#sNo').text(data.sNo);
					$('div#mTime').text(data.mTime);
					$('div#level').text(data.level);
					},'json');
					number=3;
				}
			}
		redirect(3);

		});

	</script>
	
	<script type="text/javascript">
		$(function(){
   		$('.toggler').click(function(){
		       $('th.hide_level').toggle(this.checked);
		       $('td.hide_level').toggle(this.checked);
		   });
	})

	</script>

</head>
<body>
	<!--
	<div id="box"></div>
	!-->
	<input type="checkbox" name="myCB" value="A" class="toggler" checked="checked" /> show/hide above
	<div class="container">
		<table class="table table-bordered">
	        <thead>
	          <tr>
	            <th>#</th>
	            <th>Time</th>
	            <th class="hide_level">Level</th>
	          </tr>
	        </thead>
	        <tbody>
		        <tr>
		        	<td><div id="sNo"></div></td>
		        	<td><div id="mTime"></div></td>
		        	<td class="hide_level"><div id="level"></div></td>
				</tr>
			</tbody>
		</table>
	</div>        

	<!-- ##############################-->

  <div class="container">
  <h1 class="text-center">Can I use...this service?</h1>
  </div>
</header>
<div class="container">
  <h2 class="page-header">Step 1: Where is the data?</h2>
  <div class="row">
    <div class="col-xs-12">
  <p class="lead text-center bg-info btn text-info center-block">Is the data in the system?</p>
      <div class="row">
        <div class="col-xs-6 text-center">
           <p class="btn"><span class="glyphicon glyphicon-arrow-down"></span>
        </div>
        <div class="col-xs-6 text-center">
          <p class="btn">
          <span class="glyphicon glyphicon-arrow-down"></span></p>
        </div>
      </div>

    </div>
  </div>
  <div class="row">
    <div class="col-xs-6 text-center">
  <p class="center-block"><span class="btn btn-success btn-lg">data</span></p>
      <p class="btn center-block"><span class="glyphicon glyphicon-arrow-right"></span></p>
      
      <p class="bg-success text-success btn">Okay! Proceed to step 2.</p>
    </div>
 <!-- ###################### --> 
	
</body>
</html>