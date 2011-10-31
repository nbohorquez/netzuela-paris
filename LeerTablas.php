<html>
<head>
	<title>Tablas de Netzuela</title>
</head>
<body>
	<h1>Tablas de Netzuela</h1>
	<?php
		@ $db = new mysqli('localhost','netzuela','#25pAz7_?Xx#OR9?','spuria');

		if(mysqli_connect_errno()) {
	      	die('Error de conexion (' . mysqli_connect_errno() . ') '. mysqli_connect_error());
		}
		
		$Consulta = "show tables";
		$Resultado = $db->query($Consulta);
		$NumeroDeFilas = $Resultado->num_rows;

		echo "<p>Numero de tablas: ".$NumeroDeFilas."</p>";

		for($i = 0; $i < $NumeroDeFilas; $i++) {
			$Fila = $Resultado->fetch_assoc();
			echo ($i+1).'. '.$Fila['Tables_in_spuria'].'<br/>';
		}
		
		$Resultado->free();
		$db->close();
	?>	
</body>
</html>