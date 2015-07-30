<?php
  error_reporting(E_ALL);
  ini_set('display_errors', 1);

  if(isset($_POST["logfile"])){
      $data = array("logfilename"=>$_POST["logfile"]);
      system('/usr/bin/python auth.py ' . escapeshellarg(json_encode($data)));//, $output
      //print_r( $output);
      header("Location: ../upload_logfile");
      die();
  }
  else{
    echo "no logfile to process";
      header("Location: ../upload_logfile");
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
