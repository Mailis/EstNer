<!DOCTYPE html>
<html>
<head>
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">
</head>

<body>
service receives POST
<?php
   error_reporting(E_ALL);
   ini_set('display_errors', 1);

   echo "service receives POST-> ";

   $arr = array();

   if(count($_POST) == 0){
       $_POST["url"]="http://www.duokirjastus.eu/avaleht";
       $arr["data"][0] = $_POST;
       $_POST = json_encode($arr);
   }

   system('python3 connector.py ' . escapeshellarg(json_encode($_POST)));

?>
</body>

</html> 