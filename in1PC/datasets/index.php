<?php
   error_reporting(E_ALL);
   ini_set('display_errors', 1);
   //ini_set('upload-max-filesize', '100M');
   //ini_set('post_max_size', '100M');
   //echo exec('whoami');
 
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
		<legend>Datasets</legend>
		    <?php
                        $dirname = '../datadownload/jsons/';
                        $downloads = '../datadownload/downloaded_files/';
                        if(file_exists ($dirname)){
				if ($handle = opendir($dirname)) {
				   $jsonFolders = array();
				    while (false !== ($jsonName = readdir($handle))) {
					if ($jsonName != "errors.txt" && $jsonName != "." && $jsonName != "..") {
		                            $jsonFolders[] = $jsonName;
					}
				    }//end while
				    closedir($handle);

				    sort($jsonFolders);
				    if(count($jsonFolders)>0)
				    foreach($jsonFolders as $k => $jsonName) {
					$json = json_decode(file_get_contents($dirname.$jsonName), TRUE);
					$baseUrl = $json["base_url"];
				        echo "<div style='color:#6699FF'><a href='http://$baseUrl'>" . $baseUrl . "</a></div>";
 					foreach ($json as $key => $d) {
					   if($key != "base_url"){
                                              foreach ($d as $locfname => $data) {
                                               //print_r($data);
                                               $jDate = $data["Date"];
					       if(isset($data["localFilename"]))
                                               	   $jLocalFilename = $data["localFilename"];
					       else
                                               	   $jLocalFilename = $locfname;

                                               $jTimeDir = $data["timeDir"] . "/";
                                               $jFile_url = $data["file_url"];
                                               $jType = $data["Content-Type"];
                                               $pathToLocal = $downloads . $jTimeDir . $baseUrl . "/" . $jLocalFilename;
                                                echo "<div class='remote_file'><a href='$jFile_url'>" . $jFile_url . "</a></div>";
                                                echo "<div class='remote_file'>accessed " . $jDate . "</div>";
                                                echo "<div class='remote_file'>Content-Type <span class='remote_file_type'>" . $jType . "</span> </div>";
						echo "<div class='local_file'>local dataset: <a href='$pathToLocal'>" . $jFile_url . "</a></div>";
					        }
					    }
                                         }
				    }
				}
			}
                    ?>
	        <hr><hr>
	    </div>
        </div>
    </body>
</html>
</html>
