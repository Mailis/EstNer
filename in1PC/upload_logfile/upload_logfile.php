<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

ini_set('max_execution_time', 3000000);
require_once('fileNames.php');

if (!file_exists($logFilesDir)) {
	//echo "mkdir: ";
	mkdir($logFilesDir, 0777);
    echo "<br />";
    echo "The folder $logFilesDir did not exist, created" . "<br />";
}
//----------------------------------------
$target_file = $logFilesDir . basename($_FILES["fileToUpload"]["name"]);

$uploadOk = 1;
$logFileType = pathinfo($target_file,PATHINFO_EXTENSION);
$answer = "";

if(isset($_POST["submit_logfile"])){
	// Check if file already exists
	if (file_exists($target_file)) {
	    $answer .= "<br />Sorry, file already exists. ";
	    $uploadOk = 0;
	}
	
	// Allow certain file formats
	if($logFileType != "txt" && $logFileType != "log") {
	    $answer .= "<br />Sorry, only *.txt  & *.log files are allowed. ";
	    $uploadOk = 0;
	}
//----------------------------------------
	// Check if $uploadOk is set to 0 by an error
	if ($uploadOk == 0) {
	    $answer .= "<br />Sorry, your file was not uploaded. ";
	
	} // if everything is ok, try to upload file
	else {
	    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
	        //$answer .= "<br />File ". basename( $_FILES["fileToUpload"]["name"]). " is uploaded.";
	        header("Location: index.php");
	    } 
	    else {
	        $answer .= "<br />Sorry, there was an error uploading your file.";
	        $uploadOk = 0;
	    }
	}
	echo $answer . ("<br />");
}	
else{

    echo ("No file specified!");
}
?>
<html>
<head>
<title>File was not uploaded</title>
</head>
<body>
	<?php if ($uploadOk == 0): ?>
		<h1>File was not uploaded</h1>
		<h2>File (not uploaded) info:</h2>
	<?php endif; ?>
	<ul>
		<li>File name: <?php echo $_FILES['fileToUpload']['name'];  ?>
		<li>File size: <?php echo $_FILES['fileToUpload']['size'];  ?> bytes
		<li>File type: <?php echo $_FILES['fileToUpload']['type'];  ?>
	</ul>
</body>
</html>
