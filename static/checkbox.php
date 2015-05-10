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
		       $('div#hide_time').toggle(this.checked);
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
	            <th>Level</th>
	          </tr>
	        </thead>
	        <tbody>
		        <tr>
		        	<td><div id="sNo"></div></td>
		        	
		        	<div id="hide_time">
		        		<td>
		        			<div id="mTime"></div>
		        		</td>
		        	</div>
		        	
		        	<td><div id="level"></div></td>
				</tr>
			</tbody>
		</table>
	</div>        
	
</body>
</html>