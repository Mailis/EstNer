<?php
    error_reporting(E_ALL); 
    ini_set('display_errors', 1);


$excelsdir = "downloaded_files";

$folders =  scandir($excelsdir);
$excelpaths = array();
foreach($folders as $key => $folder){
    $files = scandir($folder);
    if(count($files) > 0){
        foreach($files as $k => $f)
            $nextpath = $excelsdir . "/" . $folder . "/" . $f;
            $excelpaths[] = $nextpath;
    }
} 
return($excelpaths);
?>
