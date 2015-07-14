<?php
  error_reporting(E_ALL);
  ini_set('display_errors', 1);

print_r($_POST);
  if(isset($_POST["simulate_update"])){
        system('python3 ../RDFgenerator/monthlyUpdate.py');
	header("Location: ../updates");//
        die();//
  }
?>

<!DOCTYPE HTML>
<html lang="en">
    <head>
        <meta charset="utf-8"> 
    </head>
    <body>
    </body>
</html>
