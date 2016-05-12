<?php
   if(isset($_GET["delpath"])){
        $filetodelete = unlink($_GET["delpath"]);//
	if($filetodelete){
		 header("Location: ../upload_logfile");	
	}
	else{
		echo "file deletion was not successful";
	}
   }




   if(isset($_GET["delall"])){
        shell_exec('rm -r /var/www/html/datadownload/*');
        shell_exec('rm -r /var/www/html/generated_files/*');
        shell_exec('rm -r /var/www/html/rdf_files/*');
        system('python2 deleteObjectsInBucket.py');
        //print_r($filetodelete);
	header("Location: ../upload_logfile");	
   }
?>
