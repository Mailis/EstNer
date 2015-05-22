<?php 
error_reporting(E_ALL); 
ini_set('display_errors', 1);
echo "BQtest";
$data = array("tablename"=>"crawl1000.log");
$data = array("tablename"=>"crawl.log");
//print_r( $data);
system('python2 auth.py ' . escapeshellarg(json_encode($data)));//, $output

//print_r( $output);


?>
