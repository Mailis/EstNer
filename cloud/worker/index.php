<!DOCTYPE html>
<html>
<head>
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">
</head>

<body>

<?php
/*DEBUGGING
      if(count($_POST) == 0){
          $_POST["url"]="http://www.sm.ee/sites/default/files/content-editors/ESF/finantsanaluusi_vormid.xls";
          $arr["data"][0] = $_POST;
          $_POST = json_encode($arr);
          system('python3 connector.py ' . escapeshellarg(json_encode($_POST)));
      }
*/
   if(isset($_POST)){
       system('python3 connector.py ' . escapeshellarg(json_encode($_POST)));
   }
   else{
      header('Location: rdf_files');
   }
/*
*/
?>
</body>

</html> 
