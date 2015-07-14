<?php
  error_reporting(E_ALL);
  ini_set('display_errors', 1);

  $data = array();


  if(isset($_POST["logfile"])){
	$logfile = $_POST["logfile"];
	$data = $logfile;
	/*message is in '../js/notifyUSer.js'*/
        //$message = "Wait: RDFizing of " . $logfile . ".";
        
	// Execute the python script with the JSON data
        system('python3 connector.py ' . escapeshellarg(json_encode($data)));

	//$result = system('python3 connector.py ' . escapeshellarg(json_encode($data)));
	// Decode the result
	//$resultData = json_decode($result, true);
	//print_r($resultData);
////
	header("Location: ../");
        die();
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
