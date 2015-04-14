<html>

	<head>
		<script type="text/javascript" src="http://code.jquery.com/jquery-2.1.3.min.js"></script>
		<script type="text/javascript">
			$(document).ready(function(){
				var number=10;
				var url='http://www.google.com';

				function redirect(num,addr){
					number=num;
					url=addr;
					countdown();
				}

				function countdown(){
					
					setTimeout(countdown,1000);
					$('#box').html("Redirecting in "+number+" seconds.");
					number--;
					if(number<0)
					{
						window.location = url;
						number=0;
					}
				}
			redirect(3,'http://www.google.com');

			});

		</script>

	</head>
	
	<body>
		<div id="box"></div>
	</body>
</html>