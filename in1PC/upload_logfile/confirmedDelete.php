<?php
   if(isset($_GET["delpath"])){
        $filetodelete = unlink($_GET["delpath"]);//
	if($filetodelete){
		 header("Location: index.php");	
	}
	else{
		echo "file deletion was not successful";
	}
   }


?>
