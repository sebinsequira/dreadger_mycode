<!DOCTYPE html>
<html>
<head>
	<title>Ajax db</title>
</head>
<body>
	Name: <input type="text" id="name">
	<input type="submit" id="name-submit" value="Grab">
	<div id="name-data"></div>
	<script src="http://code.jquery.com/jquery-1.8.0.min.js"></script>
	<script type="text/javascript">
		$('input#name-submit').on('click',function(){
			var name= $('input#name').val();
			if($.trim(name)!='')
			{
				$.post('ajax/name.php',{name:name},function(data){
						$('div#name-data').text(data);
				});
			}
		});
	</script> 

	
</body>
</html>