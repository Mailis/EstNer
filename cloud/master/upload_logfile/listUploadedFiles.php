<?php
require_once('fileNames.php');
$arrayOfProcessedLogfileNames = array();
if(file_exists($processed_logfilesDir)){
	if ($handle = opendir($processed_logfilesDir)) {
	    /* This is the correct way to loop over the directory. */
	    /* entry is e.g. crawl_detail4log.txt */
	    while (false !== ($entry = readdir($handle))) {
              if($entry != ".." && $entry != ".")
	          $arrayOfProcessedLogfileNames[] = getfileNameWithoutExtension($entry);
	    }
	}
}

	  closedir($handle);
if(file_exists($logFilesDir)){
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


	    asort($files);
	    $sortedfiles = $files;//array_reverse($files, true); #sorts by file creation time
	 
	    if(count($sortedfiles) > 0){
		echo "<div style='margin-bottom:10px; margin-top:-20px;'>(most recent are displayed first)</div>";
		//print_r($files);
		echo "<table border='1' style='min-width:400px; text-align:center'>";
		echo "<tr><th> filename </th><th> created </th><th> size </th><th> nr of lines </th><th> extract entities?</th><th> delete file?</th></tr>";
		
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
	              echo "<td class='nroflines' style='text-align:right' id='".implode('_-',explode('.',$logfilename))."'>";
		      echo "<img src='../css/ajax-loader.gif' />";
		      echo "</td>";
		      echo "<td>";

			echo "<form class='extr_form' action='sendToAuth.php' method='post'><input type='hidden'  name='logfile' value='" . $logFilesDir . $logfilename . "' />";
		          if(fileisProc($logfilename) == 1){
		               echo "<span class='done'>DONE </span>";
		               echo "<input type='submit'  value='Yes, do again.' name='start_get_entities'/></form>";
		          }
		          else{
		               echo "<input type='submit'  value='Yes, extract.' name='start_get_entities'/></form>";
		          }
		      echo "</td>";
		      echo "<td>";
		        if($logfilename != "crawl.log"){
			   echo "<form action='delete_files.php' method='post'><input type='hidden'  name='logfile' value='$logfilename' />";
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
	     echo "<span class='fname_data'>No log files are uploaded yet</span>";
	  }
	  
	}//if handle

}
else{
    echo "<span class='fname_data'>No log files are uploaded yet</span>";
}



function human_filesize($bytes, $decimals = 2) {
  $sz = 'BKMGTP';
  $factor = floor((strlen($bytes) - 1) / 3);
  return sprintf("%.{$decimals}f", $bytes / pow(1024, $factor)) . @$sz[$factor];
}

function getRespectiveURLfile($logfilename){
   return getfileNameWithoutExtension($logfilename) . ".txt";
}

function fileisProc($logFname){
    //$logFname may be e.g crawl_detail4.log
    global $arrayOfProcessedLogfileNames; //e.g [crawl_detail4log]  (from crawl_detail4log.txt)
    $logfimpl = implode('',explode('.',$logFname));//e.g crawl_detail4 (crawl_detail4log from crawl_detail4.log)
               //($needle, array $haystack)
    if(in_array($logfimpl, $arrayOfProcessedLogfileNames))
             return(1);
    else
             return(0);
}

function getNrOfLines($file)
{
    $f = fopen($file, 'rb');
    $lines = 0;

    while (!feof($f)) {
        $lines += substr_count(fread($f, 8192), "\n");
    }

    fclose($f);

    return $lines;
}
?>
