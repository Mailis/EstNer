<?php
   // header("Content-Type: text/plain");
   // error_reporting(E_ALL);
   // ini_set('display_errors', 1);


    if(isset($_GET['sparql'])){
	$format = "nt";//$_GET['format'];
	$sparql = $_GET['sparql'];
        $result = get_pyresponse($format, $sparql);

	if(empty($result)){
	   deliver_response(200,  "OK", NULL);
	}
	else{
	   deliver_response(200,  "NOT OK", $result);
	}
    }
    else{
	deliver_response(200,  "invalid request", NULL);
    }
    
    function deliver_response($status,  $status_message, $data){
	header("HTTP/1.1 $status $status_message");
	$response['status'] = $status;
	$response['status_message'] = $status_message;
	$response['data'] = $data; 

	//echo json_encode($response);
    }


    function get_pyresponse($format, $sparql){
         $data["format"] = $format;
         $data["sparql"] = $sparql;
         $result = system('python3 ../sparqlservice.py ' . escapeshellarg(json_encode($data)));
         return $result;
    }
?>
