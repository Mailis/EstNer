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
		<legend>Select a Log File to Upload: </legend>
                Although only web-address is sufficient, this app works only if the uploaded log file is built following this structure:
                <br />
                <a href="http://crawler.archive.org/articles/user_manual/glossary.html#discoverypath">http://crawler.archive.org/articles/user_manual/glossary.html#discoverypath</a>
                <br />example of 2 rows, columns are separated by whitespaces:<br />
                <pre><div class="example">2014-05-08T21:35:57.220Z 1 58 dns:www.autolaige.ee P http://www.autolaige.ee/ text/dns #048 20140508213556681+234 sha1:C2LVXEPH6TEQROI4UA62E5U35432MVJO - content-size:58
                 </div>
                 <div class="example">
2014-05-08T21:35:57.221Z 1 56 dns:www.kennelklubi.ee P http://www.kennelklubi.ee/ text/dns #011 20140508213556815+99 sha1:BEEOVLNXU5RXV2Q5XIGQUB6F4EJYOVIU - content-size:56</div></pre>
                <br />
		<form action="upload_logfile.php" method="post" enctype="multipart/form-data">
		    <input type="file" name="fileToUpload" id="fileToUpload">
		    <br />
		    <input type="submit" value="Upload File" name="submit_logfile"/>
		</form>
	        <hr class="item_horiz_end">
	    </div>
            <div style="clear:both"></div>
	    <div class="item_horizontal_min">
		<legend>List of Uploaded Log Files:</legend>
		<?php 
			$linedata = array();
                        $processedLogFilesDir = "../statistics/processed_logfiles/proc_log_files.txt";
			$handle = fopen($processedLogFilesDir, "r");
			if ($handle) {
			    while (($line = fgets($handle)) !== false) {
				$lineSplitted = explode(" ", $line);
				$fname = $lineSplitted[1];
				$date = $lineSplitted[0];
                                $linedata[$fname][$date]["number of jobs"] = $lineSplitted[2];
                                $linedata[$fname][$date]["time spent(h:m:s.mm)"] = $lineSplitted[3];
                                if(isset($lineSplitted[4]))
                                    $linedata[$fname][$date]["chunksize"] = $lineSplitted[4];
                                if(isset($lineSplitted[5]))
                                    $linedata[$fname][$date]["comments"] = $lineSplitted[5];
			    }

			    fclose($handle);
			} 
                      include('listUploadedFiles.php'); 
                 ?>
	    </div>

	    <div class="item_horizontal_min" style="width:450px;">
		<legend>Processed Log Files:</legend>
		    <?php
                        if(count($linedata)>0){
			    foreach($linedata as $fname => $rows){
				//fname
				$farr = explode("/", $fname);
				$len = count($farr)-1;
				$fnam = $farr[$len];
                                $path = $farr[$len-1]."/".$farr[$len];
				echo "<div class='fname'><a href='$fname'>" .$fnam . "</a></div>";
                                foreach($rows as $date => $rest){
                                    echo "<div class='fname_data'>" .$date . "</div>";
				    foreach($rest as $k => $v){
                                        echo "<div class='fname_data_finer_key'>" .$k . ": ";
                                        echo "<span class='fname_data_finer_data'>" .$v . "</span></div>";
				    }
                                }
			    }
			    
			}
		    ?>
		
	    </div>
	    <div style="clear:both"></div>
	    <div class="item_horizontal"><hr class="item_horiz_end"></div>
        </div>
    </body>
</html>
</html>
