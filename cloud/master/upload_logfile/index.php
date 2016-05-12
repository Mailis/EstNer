<?php
   error_reporting(E_ALL);
   ini_set('display_errors', 1);
   ini_set('upload_max_filesize', '10000M');
   ini_set('post_max_size', '10000M');
   ini_set('max_input_time', 30000);
   ini_set('max_execution_time', 30000);
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
 

        <link rel="stylesheet" href="../css/main.css">
	<link  rel="stylesheet"href="../css/style.css">
	<link  rel="stylesheet"href="../css/demo.css">
	<script src="../js/jq.js" type="text/javascript"></script> 
	<script src="../js/notifyUser.js" type="text/javascript"></script> 
    </head>
    <body>
	<div class="nav">
	    <?php require_once("../nav.php"); ?>
	</div>
        <div class="pody">

            <div id="notifycation_alert"></div>
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
		    <input type="file" name="fileToUpload" id="fileToUpload" />
		    <br />
		    <input type="submit" value="Upload File" name="submit_logfile" />
		</form>
	        <hr class="item_horiz_end">
	    </div>
            <div style="clear:both"></div>

            <form action='delete_files.php' method='post' style='margin-top:-22px;margin-bottom:10px'>
                <input type='hidden'  name='logfile' value='$logfilename' />
	        <button style='width:300px' name='delete_gen_files'>delete all generated files 
                     <br />(RDFs, datasets, json-meta-models and errors) 
                     <br />in order to start testing this system from scratch 
                </button>
	    </form>

	    <div class="item_horizontal_min">
		<legend>List of Uploaded Log Files:</legend>
		    <?php 
                        include('listUploadedFiles.php'); 
                    
                    ?>
	    </div>


	    <div class="item_horizontal_min" style="width:450px;">
		<legend>Processed Log Files:</legend> 
                    <div class="stat_waiter">
                        <img src='../css/ajax-loader.gif' />
                        <?php
                            //require_once('displayStatistics.php');
		        ?>
	           </div>
	    </div>
	    <div style="clear:both"></div>
	    <div class="item_horizontal"><hr class="item_horiz_end"></div>
        </div>
    </body>
</html>
</html>
