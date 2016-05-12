<?php
   error_reporting(E_ALL);
   ini_set('display_errors', 1);
   //ini_set('upload-max-filesize', '100M');
   //ini_set('post_max_size', '100M');
   //echo exec('whoami');


   $dirname = '../datadownload/jsons/';
   $downloads = '../datadownload/downloaded_files/';
   $jsonFiles = array();
   $contentTypes = array();

   $jsons_per_page = 5;
   $pageNr = 1;
   $cntnType = "";
   $host = "";
   if(isset($_GET["page"])){
       $pageNr = $_GET["page"];
       $cntnType = "";
       $host = "";
   }
   if(isset($_GET["type"])){
       $cntnType = $_GET["type"];
       $pageNr = 0;
       $host = "";
   }
   if(isset($_GET["host"])){
       $host = $_GET["host"];
       $cntnType = "";
       $pageNr = 0;
   }
   

   function displayPageNUmbers($total){
       global $pageNr;
       echo "<span class='guide'>pages:</span>";
       for($i=1; $i<=$total; $i++){
           if($i == $pageNr)
               echo "<span class = 'pagenmbrs_active' id=".$i.">" . $i . "</span>";
           else
               echo "<span class = 'pagenmbrs' id=".$i.">" . $i . "</span>";
       }
       echo "<br />";
   }
   function displayContentTypes($contArrayKeys){
       global $cntnType;
       echo "<span class='guide'>content types:</span>";
       if(count($contArrayKeys) > 0)
       foreach($contArrayKeys as $key => $ctype){
           if( strtolower(str_replace(" ", "+", $cntnType)) == strtolower($ctype) )
               echo "<span class='remote_file_type_species_active' id = ".$ctype.">" . $ctype . "</span>";
           else
               echo "<span class='remote_file_type_species' id = ".$ctype.">" . $ctype . "</span>";
       }
       echo "<br />";
   }

   function displayHostSearchForm(){
       global $host;
       if($host == "")
           echo "<input type='text' id='host_search_input' placeholder='type part of a host name for searching' />";
       else
           echo "<input type='text' id='host_search_input' placeholder='" . $host . "' />";
       echo "<input type='submit' class='host_search_btn' value=' search by host name ' />";
   }

   function paging($nr_jsons){
       global $jsonFiles, $dirname, $jsons_per_page, $pageNr, $downloads;
       sort($jsonFiles);
	    if($nr_jsons>0){
                $itemsOnPageCounter = 0;
                $itemSliceMax = $pageNr*$jsons_per_page;
                $itemSliceMin = $itemSliceMax-($jsons_per_page-1);
	        foreach($jsonFiles as $k => $jsonName) {
                    $itemsOnPageCounter++;
                    if($itemsOnPageCounter < $itemSliceMin){
                        continue;
                    }
                    if($itemsOnPageCounter > $itemSliceMax){
                        break;
                    }
		    $json = json_decode(file_get_contents($dirname.$jsonName), TRUE);
		    $baseUrl = $json["base_url"];
		    echo "<div style='color:#6699FF'><a href='http://$baseUrl'>" . $baseUrl . "</a></div>";
		    foreach ($json as $key => $jsonitem) {
		        if($key != "base_url"){
                            displayJsonItem($jsonitem, $baseUrl);
		        }//if
                    }//foreach
		}//foreach json-folder
            }//if count(json-folder)>0

   }

   function displayJsonItem($jsonitem, $baseUrl){
      //print_r($jsonitem);
      global $downloads;
      foreach ($jsonitem as $locfname => $data) {
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
	echo "<div class='local_file'>local dataset: <a href='$pathToLocal'>" . $jLocalFilename . "</a></div>";
      }//foreach
   }

   function pageByContentType($nr_jsons){
       global $jsonFiles, $dirname, $contentTypes;
       sort($jsonFiles);
	    if($nr_jsons>0){
	        foreach($jsonFiles as $k => $jsonName) {
		    $json = json_decode(file_get_contents($dirname.$jsonName), TRUE);
		    
		    foreach ($json as $key => $jsonItem) {
		        if($key != "base_url"){
                            foreach ($jsonItem as $locfname => $data) {
                               $jType = strtolower(preg_split('/;/',$data["Content-Type"])[0]);
                               if(!in_array($jType, $contentTypes)){
                                   $contentTypes[$jType][$json["base_url"]] = $jsonItem;
                               }
                            }//foreach
		        }//if
                    }//foreach
		}//foreach json-file
            }//if nr_json-files>0
       ksort($contentTypes);
   }


   function displayCertainContentFiles($contType){
       global $contentTypes;
       
       if(count($contentTypes[$contType]) > 0)
       foreach($contentTypes[$contType] as $baseUrl => $jsonitem){
           displayJsonItem($jsonitem, $baseUrl);
       }
   }

   function displayCertainHost($hostname){
       global $jsonFiles, $dirname;
       
       if(count($jsonFiles) > 0)
       foreach($jsonFiles as $key => $jsonName){
           if (strpos($jsonName, $hostname) !== FALSE){
	        $json = json_decode(file_get_contents($dirname.$jsonName), TRUE);
	        $baseUrl = $json["base_url"];
		foreach ($json as $key => $jsonItem) {
		    if($key != "base_url"){
                        displayJsonItem($jsonItem, $baseUrl);
		    }//if
                }//foreach
           }
       }
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
	<script src="../js/datasets.js" type="text/javascript"></script> 
    </head>
    <body>
	<div class="nav">
	    <?php require_once("../nav.php"); ?>
	</div>
        <div class="pody">
	    <div class="item_horizontal">
		<legend>Datasets</legend>
		    <?php
                        if(file_exists ($dirname)){
				if ($handle = opendir($dirname)) {
				    while (false !== ($jsonName = readdir($handle))) {
					if ($jsonName != "errors.txt" && $jsonName != "." && $jsonName != "..") {
		                            $jsonFiles[] = $jsonName;
					}//end if
				    }//end while
				    closedir($handle);
                                    //page numbers
                                    $nr_jsons = count($jsonFiles);
				    if($nr_jsons>0){
					$nr_pages = $nr_jsons/$jsons_per_page;
					if($nr_jsons%$jsons_per_page != 0){
					    $nr_pages ++;
					}
                                    }
				    displayPageNUmbers($nr_pages);
                                    echo "<hr>";
                                    pageByContentType($nr_jsons);
                                    displayContentTypes(array_keys($contentTypes));
                                    echo "<hr>";
                                    displayHostSearchForm();
                                    echo "<hr>";
                                    
                                    if($cntnType != ""){
                                        displayCertainContentFiles(str_replace(" ", "+", $cntnType));
                                    }
                                    if($host != ""){
                                        displayCertainHost($host);
                                    }
                                    //query by page nr
                                    else if(is_numeric($pageNr)){
                                        paging($nr_jsons);
                                    }
				    
				}//if handle
			}//if jsons-dir exists
                    ?>
	        <hr><hr>
	    </div>
        </div>
    </body>
</html>
</html>
