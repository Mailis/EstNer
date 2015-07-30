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

   echo "service receives task to delete RDF files in worker-> ";
   shell_exec('rm -r /var/www/html/rdf_files/*');
   shell_exec('rm -r /var/www/html/downloaded_files/*');

?>
</body>

</html> 
