<?php
require_once('fileNames.php');

if(file_exists($processed_logfilesDir)){
	if ($handle = opendir($processed_logfilesDir)) {
	    /* This is the correct way to loop over the directory. */
	    while (false !== ($entry = readdir($handle))) {
                if( $entry == ".." || $entry == ".") continue;
		$fPath = $processed_logfilesDir . $entry;
		//print filename
                echo "<div class='fname' id = '".$entry."' onclick='tog(this.id)'><hr><a href='$fPath'>" . $entry . "</a></div>";
                echo "<div class='filetoggle'>";
		//read file line by line
                $filehandle = fopen($fPath, "r");
		if ($filehandle) {
		    while (($line = fgets($filehandle)) !== false) {
			// process the line read.
                        //header
                        if($line{0} == 2 && $line{1} == 0){//date
                            echo "<div class='fname_data'>" .$line . "</div>";
                        }
                        else if(strpos($line, ":")){
                            $piisis = explode(":", trim($line));
                            if(count($piisis) < 2){//big header
                                echo "<div class='fname_data_finer_key'>" . substr($piisis[0], 0, -1) . "</div>";
                            }
                            else if(count($piisis) > 1){
                                 $nextIndex = strlen($piisis[0])-1;
                                 echo "<div>" . $line . "</div>";
                            }
                        }
                        else if(strpos($line, "---") !== false){
                            echo "<div class='fname_data_finer_data'>" . $line . "</div>";
                        }
                        else if(strpos($line, "###") !== false){
                            echo "<div class='fname_data_finer_data'>" . $line . "</div>";
                        }
                        else 
                            echo "<div class='fname_data_finer_key'>" . $line . "</div>";
                        
                        
		    }//while

		    fclose($filehandle);
		}//if filehandle
                echo "</div>";// class='filetoggle'
	    }//while
            closedir($handle);
	}//if opendir

        else{
            echo "<span class='fname_data'>No processing statistics to show</span>";
        }
}//if file_exists
else{
    echo "<span class='fname_data'>No processing statistics to show</span>";
}
	  
?>
