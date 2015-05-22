<?php
   error_reporting(E_ALL);
   ini_set('display_errors', 1);
   //ini_set('upload-max-filesize', '100M');
   //ini_set('post_max_size', '100M');
   //echo exec('whoami');
 
?>
<?php

$upperFolder = "../upload_logfile/generated_files/";

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
	    foreach($dirarr as $key => $value){
		$l = $dirname . $value;
	    	echo "<li><div class='error_item'><a href='$l'>" . $value . "</a></div></li>";
	    }
	    echo"</ul>";
	}
	else{ echo "nothing to show";}

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
	    <div class="item_horizontal_min_error">
		<legend>opening URL errors:</legend>
		    <a href = "../datadownload/jsons/errors.txt">read URL errors</a>
		    <br />
		    <?php
                        $dirname = '../datasets/jsons/';
                        if(file_exists ($dirname)){
				if ($handle = opendir($dirname)) {
				    while (false !== ($entry = readdir($handle))) {
					if ($entry != "." && $entry != "..") {
		                            $linkToFile = $entry. "/errors.txt";
		                            if(file_exists ($linkToFile)){
						echo "<div style='color:#6699FF'><a href='$linkToFile'>" . $linkToFile . "</a></div>";
		                            }
					}
				    }
				    closedir($handle);
				}
			}
		    ?>
	        <hr><hr>
	    </div>
	    <div class="item_horizontal_min_error">
		<legend>download errors:</legend>
                    <?php $dirname = $upperFolder.'download_errors/'; ?>
		    <a class="cap" href = "<?= $dirname; ?>">download errors folder</a>
		    <br />
		    <?php echoErrors($dirname) ?>
	        <hr><hr>
	    </div>

	    <div class="item_horizontal_min_error">
		<legend>parsing documents at some URL errors: </legend>
                    <?php $dirname = $upperFolder.'parsing_errors/'; ?>
		    <a class="cap" href = "<?= $dirname; ?>">parsing errors folder</a>
		    <br />
		    <?php echoErrors($dirname) ?>
	        <hr><hr>
	    </div>

	    <div class="item_horizontal_min_error">
		<legend>programming errors:</legend>
                <?php $dirname = $upperFolder.'programming_errors/'; ?>
		<a class="cap" href = "<?= $dirname; ?>">programming errors folder</a>
		    <br />
		    <?php echoErrors($dirname) ?>
	        <hr><hr>
	    </div>

	    <div class="item_horizontal_min_error">
		<legend>RDF creation errors:</legend>
                <?php $dirname = $upperFolder.'tripling_errors/'; ?>
		<a class="cap" href = "<?= $dirname; ?>">RDF errors folder</a>
		    <br />
		    <?php echoErrors($dirname) ?>
	        <hr><hr>
	    </div>

	    <div class="item_horizontal_min_error">
		<legend>update errors:</legend>
                <?php $dirname = $upperFolder.'update_errors/'; ?>
		<a class="cap" href = "<?= $dirname; ?>">update errors folder</a>
		    <br />
		    <?php echoErrors($dirname) ?>
	        <hr><hr>
	    </div>
        </div>
    </body>
</html>
</html>
