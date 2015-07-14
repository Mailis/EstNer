<?php
   error_reporting(E_ALL);
   ini_set('display_errors', 1);
   //ini_set('upload-max-filesize', '100M');
   //ini_set('post_max_size', '100M');
   //echo exec('whoami');
   session_start();
?>
<?php

$upperFolder = "../statistics/";
//data in all lines of all files
$lineArray = array();

function dirToFileArray($dir) {
  
   $result = array();

   $cdir = scandir($dir);
   foreach ($cdir as $key => $value)
   {
      if (!in_array($value,array(".","..")))
      {
         if (is_dir($dir . DIRECTORY_SEPARATOR . $value))
         {
            $result[$value] = dirToFileArray($dir . DIRECTORY_SEPARATOR . $value);
         }
         else
         {
            $result[] = $value;
         }
      }
   }
  
   return $result;
}


function echoUpdateStats($dirname){
    global $lineArray;
    $filesarr=dirToFileArray($dirname);
    if(count($filesarr) > 0)
    foreach($filesarr as $key => $filename){
        readUPDfile($dirname . $filename);
    }
    //print_r($lineArray);
    $lineArrLen = count($lineArray);
    if($lineArrLen > 0){
        $tableHeaders = array_keys($lineArray[($lineArrLen-1)]);
        echo "<table class = 'update_table' border=1 ><tr>";
        foreach($tableHeaders as $key => $colhead){
            echo "<th>" . $colhead . "</th>";
        }
        echo "</tr>";
        foreach($lineArray as $key => $row){
            echo "<tr bgcolor='#CFF'align='center'>";
            foreach($row as $k => $cell){
                if($k == "date")
                    echo "<td>" . implode(" ", explode("_", $cell)) . "</td>";
                else
                    echo "<td>" . $cell . "</td>";
            }
            echo "</tr>";
        }
        echo "</table>";
    }
    else{ echo "nothing to show";}
}

function readUPDfile($filename){
    global $lineArray;
    $handle = fopen($filename, "r");
    if ($handle) {
        //data in one line
        $linedata = array();
	while (($line = fgets($handle)) !== false) {
		$lineSplitted = explode(" ", $line);
                $linedata["date"] = $lineSplitted[0];
                $linedata["number of jobs"] = $lineSplitted[1];
                $linedata["time spent(h:m:s.mm)"] = $lineSplitted[2];
                if(isset($lineSplitted[3]))
                    $linedata["chunksize"] = $lineSplitted[3];
                if(isset($lineSplitted[4]))
                    $linedata["nr of changes"] = $lineSplitted[4];
                if(isset($lineSplitted[5]))
                    $linedata["download start"] = $lineSplitted[5];
                if(isset($lineSplitted[6]))
                    $linedata["nr of downloads"] = $lineSplitted[6];
                if(isset($lineSplitted[7]))
                    $linedata["time spent on downloading"] = $lineSplitted[7];
                $lineArray[] = $linedata;
        }
        fclose($handle);
    } 
    return $lineArray;
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

        <link rel="stylesheet" href="../css/main.css">
        <link rel="stylesheet" href="../css/demo.css">
	<link  rel="stylesheet"href="../css/style.css">
	<script src="../js/jq.js" type="text/javascript"></script> 
	<script src="../js/notifyUser.js" type="text/javascript"></script>
    </head>
    <body>
	<div class="nav">
	    <?php require_once("../nav.php"); ?>
	</div>
        <div class="pody">
	    <div class="item_horizontal">
		<legend>Simulate monthly updates
                <form action="simulate_update.php" method='post' id="simulate_update">
                    <input type="submit" value="simulate" name="simulate_update"/>
                </form>
                </legend>
                <div id="notifycation_alert_simulate"></div>
		<legend>Monthly updates statistics</legend>
                    <?php $dirname = $upperFolder.'monthly_updates/'; ?>
	    
	            <?php echoUpdateStats($dirname) ?>
	    </div>

        </div>
    </body>
</html>
</html>
