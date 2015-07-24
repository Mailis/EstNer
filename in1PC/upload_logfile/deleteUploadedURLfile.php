<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
require_once('fileNames.php');

if(isset($_POST["delete_download"]) && isset($_POST["logfile"])){
    echo "<h1>Deletion confirmation</h1> of <b>". $_POST["logfile"]."</b>";
    $delPath = './' . $logFilesDir . $_POST["logfile"];
    redirect("confirmedDelete.php?delpath=$delPath", "This action cannot be undone. Are you sure, you want to delete ". $_POST["logfile"]."?");
}
print_r($_POST);
if(isset($_POST["delete_gen_files"])){
    echo "<h1>Deletion confirmation of all generated files (RDF, datasets, json-meta-models, errors).</b>";
    ///var/www/html/datadownload/*
    $delPath = './datadownload/*';
    redirect("confirmedDelete.php?delall=$delPath", "This action cannot be undone. Are you sure, you want to delete all generated files?");
}	
	
	

function redirect($redirect, $message) ///confirm box pop up
    {
        echo "<script>javascript:
        var ask = confirm('".$message."');
        if(ask==true)
        {
            window.location = '".$redirect."';  
        }
        else
        {
            window.location = 'index.php';    
        }
        </script>";
    }


?>
