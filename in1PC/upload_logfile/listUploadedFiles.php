<?php
require_once('fileNames.php');
if ($handle = opendir($logFilesDir)) {
  
  $files=array();
    /* This is the correct way to loop over the directory. */
    $fcounter = 0;
    while (false !== ($entry = readdir($handle))) {
      $logFileType = pathinfo($entry,PATHINFO_EXTENSION);
      //print_r($logFileType); echo "<br>";
      if($logFileType == "txt" || $logFileType == "log") {
        $fPath = $logFilesDir . $entry;
        $created = filectime ($fPath);
        $fSize = human_filesize(filesize ($fPath));
        //$files[]=array($created, $entry);
        $files[$fcounter]["name"] = $entry;
        $files[$fcounter]["size"] = $fSize;
        $files[$fcounter]["time"] = $created;
        $files[$fcounter]["path"] = $fPath;
        $fcounter++;
      }
    }

  closedir($handle);
  if ($files){

	$kiiis = array();
	if(isset($linedata)){
                  $kiis = array_keys($linedata);
                  foreach($kiis as $ck => $cpath){
                     $carr = explode("/", $cpath);
		     $len = count($carr)-1;
		     $fnam = $carr[$len];
		     $kiiis[] = $fnam;
		  }
	}


    ksort($files);
    $sortedfiles = array_reverse($files, true); #sorts by file creation time
 
    if(count($sortedfiles) > 0){
	echo "<div style='margin-bottom:10px; margin-top:-20px;'>(most recent are displayed first)</div>";
	//print_r($files);
	echo "<table border='1' style='min-width:400px; text-align:center'>";
	echo "<tr><th> filename </th><th> created </th><th> size </th><th> extract entities?</th><th> delete file?</th></tr>";
        
	foreach($sortedfiles as $counterr => $filedata){
	   $logfilename = $filedata["name"];
           $timestamp = $filedata["time"];
           $fPathh = $filedata["path"];
	   echo "<tr>";
	      echo "<td  style='color:#6699FF'><a href='$fPathh'>" . $logfilename . "</a";
	      echo "</td>";
	      echo "<td>" . date('m/d/Y H:i:s', $timestamp);
	      echo "</td>";
	      echo "<td>" . $filedata["size"] . "</td>";
	      echo "<td>";
		echo "<form class='extr_form' action='../RDFgenerator/' method='post'><input type='hidden'  name='logfile' value='" . $logFilesDir . $logfilename . "' />";
               if(count($kiiis)>0){
                  if(in_array($logfilename, $kiiis)){
                       echo "<span class='done'>DONE</span>";
                       echo "<input type='submit'  value='Yes, do again.' name='start_get_entities'/></form>";
                  }
                  else{
                       echo "<input type='submit'  value='Yes, extract.' name='start_get_entities'/></form>";
                  }
                }
                else{
		       echo "<input type='submit'  value='Yes, extract.' name='start_get_entities'/></form>";
                }
	      echo "</td>";
	      echo "<td>";
                if($logfilename != "crawl.log"){
		   echo "<form action='deleteUploadedURLfile.php' method='post'><input type='hidden'  name='logfile' value='$logfilename' />";
		   echo "<input type='submit'  value='delete' name='delete_download'/>";
		   echo "</form>";
		}
	      echo "</td>";
	   echo "</tr>";      
	}//foreach
	echo "</table>";
    }//if count($sortedfiles) > 0
  }//if files
  else{
     echo "<div style='margin-bottom:10px; margin-top:-20px;'>no log-files to display</div>";
  }
  
}//if handle



function human_filesize($bytes, $decimals = 2) {
  $sz = 'BKMGTP';
  $factor = floor((strlen($bytes) - 1) / 3);
  return sprintf("%.{$decimals}f", $bytes / pow(1024, $factor)) . @$sz[$factor];
}

function getRespectiveURLfile($logfilename){
   return getfileNameWithoutExtension($logfilename) . ".txt";
}
?>
