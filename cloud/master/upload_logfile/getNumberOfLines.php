<?php
   error_reporting(E_ALL);
   ini_set('display_errors', 1);

require_once('fileNames.php');

if(isset($_GET["id"]) && isset($_GET["filename"])){
    $file = $logFilesDir . $_GET["filename"];
    $fid = $_GET["id"];
    $nrl = getNrOfLines($file);
    $farr = array($fid => $nrl);
    echo json_encode($farr);
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
