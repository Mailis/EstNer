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




   if(isset($_GET["delall"])){
        $filetodelete = shell_exec('rm -r /var/www/html/datadownload/*');
        $filetodelete = shell_exec('rm -r rm -r /var/www/html/generated_files/*');
        $filetodelete = shell_exec('rm -r /var/www/html/rdf_files/*');
        //print_r($filetodelete);
	header("Location: index.php");	
   }
?>
