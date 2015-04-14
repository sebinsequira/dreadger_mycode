<!DOCTYPE html>
<html>
<head>
	<script type="text/javascript" src="http://code.jquery.com/jquery-2.1.3.min.js"></script>
	<script type="text/javascript">
		$( document ).ready(function() {
    		myFunction();
		});
	</script>

	<script type="text/javascript">
		function myFunction() {
    	alert("Hello! I am an alert box!");
		var number=10;
		var url='';

		function countdown(){
			setTimeout(countdown,1000);
			$('#box').html("Redirecting in"+number+" seconds.");
			number--;
		}
		countdown();
		}

	</script>
</head>

<body>

<p>Click the button to display an alert box.</p>

<button onclick="myFunction()">Try it</button>

<div id="box"></div>
</body>
</html>
