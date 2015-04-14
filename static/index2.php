<!DOCTYPE html>
<html>
<head>
	<title>Ajax db</title>
	
</head>
<body>
	Name: <input type="text" id="name">
	<input type="submit" id="name-submit" value="Grab">
	
	<table class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>mTime</th>
            <th>IP</th>
          </tr>
        </thead>
        <tbody>
        <tr>
        	<td><div id="sNo"></div></td>
        	<td><div id="mTime"></div></td>
        	<td><div id="level"></div></td>
        </tr>
	

	<script src="http://code.jquery.com/jquery-1.8.0.min.js"></script>
	<script type="text/javascript">
		$('input#name-submit').on('click',function(){
			var name= $('input#name').val();
			if($.trim(name)!='')
			{
				$.post('ajax/name2.php',{name:name},function(data){
						$('div#sNo').text(data.sNo);
						$('div#mTime').text(data.mTime);
						$('div#level').text(data.level);
				},'json');
			}
		});
	</script> 

	
</body>
</html>