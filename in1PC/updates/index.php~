<?php
   error_reporting(E_ALL);
   ini_set('display_errors', 1);
   //ini_set('upload-max-filesize', '100M');
   //ini_set('post_max_size', '100M');
   //echo exec('whoami');
 
?>
<?php

$upperFolder = "../statistics/";

function dirToArray($dir) {
  
   $result = array();

   $cdir = scandir($dir);
   foreach ($cdir as $key => $value)
   {
      if (!in_array($value,array(".","..")))
      {
         if (is_dir($dir . DIRECTORY_SEPARATOR . $value))
         {
            $result[$value] = dirToArray($dir . DIRECTORY_SEPARATOR . $value);
         }
         else
         {
            $result[] = $value;
         }
      }
   }
  
   return $result;
}


function echoErrors($dirname){
        $dirarr=dirToArray($dirname);
	if(count($dirarr) > 0){
	    echo"<ul>";
	    foreach($dirarr as $key => $filename){
		$l = $dirname . $filename;
	    	//echo "<li><div class='error_item'><a href='$l'>" . $value . "</a></div></li>";
                echoUPDstatistics($l);
	    }
	    echo"</ul>";
	}
	else{ echo "nothing to show";}

}

function readUPDfile($filename){
        $linedata = array();
	$handle = fopen($filename, "r");
	if ($handle) {
	    while (($line = fgets($handle)) !== false) {
		$lineSplitted = explode(" ", $line);
                $linedata["date"] = $lineSplitted[0];
                $linedata["number of jobs"] = $lineSplitted[1];
                $linedata["time spent(h:m:s.mm)"] = $lineSplitted[2];
                if(isset($lineSplitted[3]))
                    $linedata["chunksize"] = $lineSplitted[3];
	    }

	    fclose($handle);
	} 
	return $linedata;
}


function echoUPDstatistics($filename){
        $linedata = readUPDfile($filename);
        echo "<table border=1>";
        echo "<tr><th>date</th><th>number of jobs</th><th>time spent (h:m:s.mm)</th><th>chunksize</th></tr>";
	echo"<tr bgcolor='#CFF'align='center'>";
	foreach($linedata as $key => $value){
            echo "<td>$value</td>";
	}
	echo"</tr>";
        echo "</table>";
}
?> 
<!DOCTYPE HTML>

<html lang="en">
    <head>
        <meta charset="utf-8"> 
	<!-- Force latest IE rendering engine or ChromeFrame if installed -->
	<!--[if IE]>
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<![endif]-->
	<title>Cloud Infrastructure for Linked Estonian Government Open Data</title>
	<meta name="description" content="Cloud Infrastructure for Linked Government Open Data.">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	 
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js" type="text/javascript"></script>
	<!-- Bootstrap styles -->
	<script type="text/javascript" src="../js/jquery-1.11.2.min.js"></script> 
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">

	<link rel="stylesheet" href="../upload.css">

        <link rel="stylesheet" href="../css/main.css">
        <link rel="stylesheet" href="../css/demo.css">
	<link  rel="stylesheet"href="../css/style.css">
	<script src="../js/jq.js" type="text/javascript"></script> 
    </head>
    <body>
	<div class="nav">
	    <?php require_once("../nav.php"); ?>
	</div>
        <div class="pody">
	    <div class="item_horizontal">
		<legend>Monthly updates statistics</legend>
                    <?php $dirname = $upperFolder.'monthly_updates/'; ?>
	    
	            <?php echoErrors($dirname) ?>
	    </div>

        </div>
    </body>
</html>
</html>
