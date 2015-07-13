<?php
//folder for storing files that include different url on each line
$parsedUrlsDir = "../url_list/";
//folder for storing uploaded log-files
$logFilesDir = "../logfiles/";
//folder for downloaded urls
$downloadsDir = "../downloads_wget/";
function getfileNameWithoutExtension($logfilename){
  $nameWithoutExtension = "";
  $strArray = explode("." , $logfilename);
  for($i=0; $i < (count($strArray)-1); $i++){
    $nameWithoutExtension .= $strArray[$i];
  }
  return $nameWithoutExtension;
}  

?>
