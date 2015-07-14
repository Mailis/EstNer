<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
require_once('fileNames.php');

echo "<h1>Deletion confirmation</h1> of <b>". $_POST["logfile"]."</b>";
if(isset($_POST["delete_download"]) && isset($_POST["logfile"])){
    $delPath = './' . $logFilesDir . $_POST["logfile"];
    redirect("confirmedDelete.php?delpath=$delPath", "This action cannot be undone. Are you sure, you want to delete ". $_POST["logfile"]."?");
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
