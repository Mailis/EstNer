<?php
    header('Content-Type: application/json; charset=utf-8');
    // header("Content-Type: application/json");
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
 
    if(isset($_POST['sparql'])){
	$format = "json";//$_GET['format'];
	$sparql = $_POST['sparql'];
        //echo json_encode(array("siin see on!" . $sparql), JSON_UNESCAPED_UNICODE);
        
        $result = get_pyresponse($format, $sparql);

	if(empty($result)){
	   deliver_response(200,  "response is empty", NULL);
	}
        else{
	    echo $result;
	}
/**/
    }

    else{
	deliver_response(200,  "invalid request", NULL);
    }
/**/    
    function deliver_response($status,  $status_message, $data){
	header("HTTP/1.1 $status $status_message");
	$response['status'] = $status;
	$response['status_message'] = $status_message;
	$response['data'] = $data; 

	echo json_encode($response);
    }


    function get_pyresponse($format, $sparql){
         $data["format"] = $format;
         $data["sparql"] = str_replace('"', "'", str_replace("\r\n", " ", $sparql));//$sparql;//
         $jsoned = (json_encode($data));
         $result = exec('python3 ../sparqlservice.py ' . escapeshellarg($jsoned));
         return ($result);
    }
?>
