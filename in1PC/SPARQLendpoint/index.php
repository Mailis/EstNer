<?php 
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
    
    $urrors = "";
    $scndurrors = "";

//////first column: insert object type and/or object name
    $fieldvalues = array("tyypradio" => "", "locname" => "", "orgname" => "", "pergname" => "", "perfname" => "");
    if(isset($_GET["tyypradio"]))
	$fieldvalues["tyypradio"] = $_GET["tyypradio"];
    if(isset($_GET["locname"]) && $fieldvalues["tyypradio"]=="loc")
	$fieldvalues["locname"] = $_GET["locname"];
    if(isset($_GET["orgname"]) && $fieldvalues["tyypradio"]=="org")
	$fieldvalues["orgname"] = $_GET["orgname"];
    if($fieldvalues["tyypradio"]=="per"){
	if(isset($_GET["pergname"]))
	    $fieldvalues["pergname"] = $_GET["pergname"];
	if(isset($_GET["perfname"]))
	    $fieldvalues["perfname"] = $_GET["perfname"];
    }
//////second column: insert webpage and object type(s)
    $webpagevalues = array("uri" => "", "checkloc" => "", "checkorg" => "", "checkper" => "");
    if(isset($_GET["uri"]))
	$webpagevalues["uri"] = $_GET["uri"];
    if(isset($_GET["checkloc"]))
	$webpagevalues["checkloc"] = $_GET["checkloc"];
    if(isset($_GET["checkorg"]))
	$webpagevalues["checkorg"] = $_GET["checkorg"];
    if(isset($_GET["checkper"]))
	$webpagevalues["checkper"] = $_GET["checkper"];
   
//////structuretypes
    $structuretypes = array("json" => "", "xml" => "", "turtle" => "", "ntriples" => "", "n3" => "");
?>

<?php 
//////first column: validate inserted data
    if( isset($fieldvalues["tyypradio"]) ){
        //print_r($_GET);
        
	if( $fieldvalues["tyypradio"] == "loc" ){
           if($fieldvalues["locname"] != ""){
	       if($urrors != ""){
		   $urrors = "";
	       }
           }
	    else{
	        $urrors = "";//"Fill name field for location";
	    }
        }
	if(  $fieldvalues["tyypradio"] == "org"  ){
           if($fieldvalues["orgname"] != ""){
	       if($urrors != ""){
		   $urrors = "";
	       }
           }
	    else{
	        $urrors = "";//"Fill name field for organization";
	    }
        }
	if($fieldvalues["tyypradio"] == "per"){
		if($fieldvalues["pergname"] != "" || $fieldvalues["perfname"] != "" ){
	           if($urrors != ""){
			$urrors = "";
	           }
	        }
                else if($fieldvalues["pergname"] == "" && $fieldvalues["perfname"] == "" ){
	            $urrors = "";//"Fill at least 1 name for person";
	        }
	}


    $data = array();


//////second column: validate inserted data
    if(isset($_GET["uri"])){
        $url = $webpagevalues["uri"];
	if(isset($webpagevalues["uri"])){
	    if($webpagevalues["checkloc"]=="" && $webpagevalues["checkorg"]=="" && $webpagevalues["checkper"]==""){
		$scndurrors = "Select at least 1 checkbox";
	    }
	    else if($url == "http://"){
	        $scndurrors = "Insert URL";
	    }
            else if($webpagevalues["checkloc"] != "" || $webpagevalues["checkorg"] != "" || $webpagevalues["checkper"] != ""){
		if($url == "" || $url == "http://www")
		{
		    $scndurrors = "URL is not valid";
		}
		else{
                    $lastIndex = strlen($url)-1;
                    if($url[$lastIndex] != "/"){
                        $url = $url . "/";
                    }
	///////////////// SECOND COLUMN DATA 
		    $scndurrors = "";
		    $data["scnd"]["uri"] = $url;
		    $data["scnd"]["loc"] = ($webpagevalues["checkloc"]=="" ? False : True);
		    $data["scnd"]["org"] = ($webpagevalues["checkorg"]=="" ? False : True);
		    $data["scnd"]["per"] = ($webpagevalues["checkper"]=="" ? False : True);
		}
	    }
	}
    }   
       

	///////////////// FIRST COLUMN DATA 
	if($fieldvalues["tyypradio"] == "loc" && $fieldvalues["locname"] != ""){
            $data["fst"] = array(array($fieldvalues["locname"]), 'loc');
        }
        else if($fieldvalues["tyypradio"] == "org" && $fieldvalues["orgname"] != ""){
            $data["fst"] = array(array($fieldvalues["orgname"]), 'org');
        }
	else if($fieldvalues["tyypradio"] == "loc" && $fieldvalues["locname"] == ""){
            $data["fst"] = array(array(0=>"null"), 'loc');
        }
        else if($fieldvalues["tyypradio"] == "org" && $fieldvalues["orgname"] == ""){
            $data["fst"] = array(array(0=>"null"), 'org');
        }
        else if($fieldvalues["tyypradio"] == "per" && $fieldvalues["pergname"] == "" && $fieldvalues["perfname"] == ""){
	    $data["fst"] = array(array(0=>"null"), "per");
	}
        else if($fieldvalues["tyypradio"] == "per"){
	    $param = array();
	    if($fieldvalues["pergname"] != "")
	        $param["gname"] = $fieldvalues["pergname"];
	    if($fieldvalues["perfname"] != "")
	        $param["fname"] = $fieldvalues["perfname"];
	    $data["fst"] = array(array(0=>$param), "per");
	}

        //print_r($data);
///////////////// SEND DATA TO PYTHON SCRIPT 
	//print_r($data);

	if(count($data) > 0){
            //print_r($data);
	    // Execute the python script with the JSON data
	    $result = exec('python3 owlyQuery2.py ' . escapeshellarg(json_encode($data)));

	    // Decode the result
	    $resultData = json_decode($result, true);
	    //print_r($resultData);
        }
	    
    }


        //TESTS		    
	// This is the data you want to pass to Python
        /*
	//$data = array("Soome laht", 'loc');
	//$data = array("MTÜ DUO kirjastus, 'org');
	//$param = array();
	//$param["gname"] = "Mailis";
	//$param["fname"] = "Toompuu";
	//$data = array($param, $fieldvalues["tyypradio"]);
        */
	//send variables
?>
<!DOCTYPE html>
<html lang="et">
<head>
        <meta charset="utf-8"> 
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <link href="css/main.css" rel="stylesheet">
        <link href="css/demo.css" rel="stylesheet">
	<link rel="stylesheet" href="../css/style.css">
	<link rel="stylesheet" href="css/style.css">
	<script type="text/javascript" src="js/jquery-1.11.2.min.js"></script> 
	<script type="text/javascript" src="js/jq.js"></script> 
</head>
    <body>
	<div class="nav">
	    <?php require_once("../nav.php"); ?>
	</div>
    <div class="pody">
<!------------------------_______SEARCH FOR OBJECTS________________------------------------------------> 
        <div class="item">
            <form name="typeform" method="get">
                <fieldset>
                    <legend>What type of object do you want to query for?</legend>

<!------------------------_______RADIOS_______________------------------------------------> 
                        <?php if($fieldvalues["tyypradio"]=="loc"): ?>
                       	    <input id="rloc" type="radio" name="tyypradio" value="loc" checked />
			<?php else: ?>
                       	    <input id="rloc" type="radio" name="tyypradio" value="loc" />
			<?php endif; ?>
		<!-------------------->
                         <label for="rloc">Locations</label> <br />
                        <?php if($fieldvalues["tyypradio"]=="org"): ?>
                            <input id="rorg" type="radio" name="tyypradio" value="org" checked />
			<?php else: ?>
                            <input id="rorg" type="radio" name="tyypradio" value="org" />
			<?php endif; ?>
		<!-------------------->
                         <label for="rorg">Organizations</label> <br />
                        <?php if($fieldvalues["tyypradio"]=="per"): ?>
                            <input id="rper" type="radio" name="tyypradio" value="per" checked />
			<?php else: ?>
                            <input id="rper" type="radio" name="tyypradio" value="per" />
			<?php endif; ?>
                         <label for="rper">People</label> <br />

<!------------------------_______INPUTS________________------------------------------------> 
		<!-------------------->
			<?php if($fieldvalues["locname"] != "" && $fieldvalues["tyypradio"]=="loc"): ?>
                            <div id="loc_input" class="selectedtyyp_visible">
                                <input class="fstcol" value="<?= $fieldvalues['locname']; ?>" type="text" name="locname" placeholder="insert location name" />
                            </div>
			<?php else: ?>
                            <div id="loc_input" class="selectedtyyp">
                                <input class="fstcol" type="text" name="locname" placeholder="insert location name" />
                            </div>
			<?php endif; ?>
		<!-------------------->
			<?php if($fieldvalues["orgname"] != "" && $fieldvalues["tyypradio"]=="org"): ?>
                            <div id="org_input" class="selectedtyyp_visible">
                                <input class="fstcol" value="<?= $fieldvalues['orgname']; ?>" type="text" name="orgname" placeholder="insert organization name" />
                            </div>
			<?php else: ?>
                            <div id="org_input" class="selectedtyyp">
                                <input class="fstcol" type="text" name="orgname" placeholder="insert organization name" />
                            </div>
			<?php endif; ?>
		<!-------------------->
                        <div id="per_input" class="selectedtyyp">
                            <?php if($fieldvalues["pergname"] != "" && $fieldvalues["tyypradio"]=="per"): ?>
                                <input class="fstcol" value="<?= $fieldvalues['pergname']; ?>" id="per_input_given" type="text" name="pergname" placeholder="insert given name" />
			    <?php else: ?>
                                <input class="fstcol" id="per_input_given" type="text" name="pergname" placeholder="insert given name" />
			    <?php endif; ?>
                            <?php if($fieldvalues["perfname"] != "" && $fieldvalues["tyypradio"]=="per"): ?>
                                <input class="fstcol" value="<?= $fieldvalues['perfname']; ?>" id="per_input_family" type="text" name="perfname" placeholder="insert family name" />
			    <?php else: ?>
                                <input class="fstcol" id="per_input_family" type="text" name="perfname" placeholder="insert family name" />
			    <?php endif; ?>
                        </div>
		<!-------------------->
			<?php if($urrors != ""): ?>
			    <div id="error" class="hasError">
			        <?= $urrors; ?>
			    </div>
			<?php endif; ?>
			<br />
		<!-------------------->
                        <input type="submit" value="Perform SPARQL query" />
		<!-------------------->
                </fieldset>
	    </form>
        
	</div>

<!------------------------_______SEARCH INSIDE WEB PAGES________________------------------------------------> 
        <?php 
	     
	?>
        <div class="item">
              <form name="webpageform" method="get">
                <fieldset>
                    <legend>From what URI do you want to query for and what type of objects?</legend>
                        <?php if($webpagevalues["checkloc"] != ""): ?>
                         <input id="cloc" type="checkbox" name="checkloc" value="loc" checked />
			<?php else: ?>
                         <input id="cloc" type="checkbox" name="checkloc" value="loc" />
			<?php endif; ?>
                        <label for="cloc">Locations</label> <br />
		<!-------------------->
                        <?php if($webpagevalues["checkorg"] != ""): ?>
                         <input id="corg" type="checkbox" name="checkorg" value="org" checked />
			<?php else: ?>
                         <input id="corg" type="checkbox" name="checkorg" value="org" />
			<?php endif; ?>
                        <label for="corg">Organizations</label> <br />
		<!-------------------->
                        <?php if($webpagevalues["checkper"] != ""): ?>
                         <input id="cper" type="checkbox" name="checkper" value="per" checked />
			<?php else: ?>
                         <input id="cper" type="checkbox" name="checkper" value="per" />
			<?php endif; ?>
                        <label for="cper">People</label> <br />
		<!-------------------->
                        <?php if($webpagevalues["uri"] != ""): ?>
                            <div id="webpage_input" class="web">
                                <input value="<?= $webpagevalues['uri']; ?>" type="text" name="uri" placeholder="insert URI" />
                            </div>
			<?php else: ?>
                            <div id="webpage_input" class="web">
                                <input type="text" name="uri" placeholder="insert URI" />
                            </div>
			<?php endif; ?>
		<!-------------------->
			<?php if($scndurrors != ""): ?>
			    <div id="scnderror" class="hasError">
			        <?= $scndurrors; ?>
			    </div>
			<?php endif; ?>
			<br />
		<!-------------------->
                        <input type="submit" value="Perform SPARQL query" />
		<!-------------------->
		</fieldset>
	    </form>
        </div>
<!------------------------_______DISPLAY SPARQL QUERY SENTENCE________________------------------------------------> 
        <div class="item_sprqlsentence">
              <form id="sprqlform" method="post" action="structures">
                <fieldset>
                    <legend>SPARQL sentence</legend>
			<?php 
				$isName = 0;
				$isGname = 0;
				$isFname = 0;
				$isWebpage = 0;
				if (isset($data["fst"][0][0]) && !is_array($data["fst"][0][0])){
				    $isName = $data["fst"][0][0];
				}
				if (isset($data["fst"][0][0]["gname"])){
				    $isGname = $data["fst"][0][0]["gname"];
				}
				if (isset($data["fst"][0][0]["fname"])){
				    $isFname = $data["fst"][0][0]["fname"];
				}
				else if (isset($data["scnd"]["uri"])){
				    $isWebpage=$data["scnd"]["uri"];
				}
			?>
                          <?php if(isset($resultData) && count($resultData["qstring"]) > 0): ?>
                              <?php 
                                    $qstring_tmp = $resultData["qstring"];
                                    $qstring = $qstring_tmp; 
                              ?>
			      <?php if(!is_array($qstring_tmp)): ?>
			          <samp>
                                        <!--replace variable name in qstring-->
				      <textarea id="notype" class="sprql_textarea" name="sparql"><?php 
                                        if($isName && $isName != "null")
                                            $qstring = str_replace("?name", '"' . $isName . '"', $qstring_tmp);
                                        if($isGname)
                                            $qstring = str_replace("?gname", '"' . $isGname . '"', $qstring_tmp);
                                        if($isFname)
                                            $qstring = str_replace("?fname", '"' . $isFname . '"', $qstring_tmp);
                                        if($isWebpage)
                                            $qstring = str_replace("?webpage", '<' . $isWebpage . '>', $qstring_tmp);
				    	echo $qstring;?></textarea>
			          </samp>
                                    <!--second column: web page data-->
			      <?php else: ?>                                     
				<!-- tabs -->
				<div class="tabs">
				  <?php $counter=0; ?>
                                  <?php foreach($qstring_tmp as $qtype => $qstring): ?>
                                        <?php 
                                             if ($qtype == "loc") $qtype = "locations";
                                             else if ($qtype == "org") $qtype = "organizations";
                                        ?>
					<?php $counter++; ?>
					<?php if($counter==1): ?>
				            <a href="#" data-tab="<?= $counter; ?>" class="tab active"><?= $qtype; ?></a>
					<?php else: ?>
				            <a href="#" data-tab="<?= $counter; ?>" class="tab"><?= $qtype; ?></a>
					<?php endif; ?>
                                  <?php endforeach; ?>
				  <?php $counter=0; ?>
                                  <?php foreach($qstring_tmp as $qtype => $qstring): ?>
                                    <?php 
                                        /**/
                                        if($isWebpage){
                                            $qstring = str_replace("?webpage", '<' . $isWebpage . '>', $qstring);
					}
                                        
				    ?>
                                        <?php 
                                             if ($qtype == "loc") $qtype = "locations";
                                             else if ($qtype == "org") $qtype = "organizations";
                                        ?>
					<?php $counter++; ?>
					<?php if($counter==1): ?>
				            <div data-content="<?= $counter; ?>" class="content active">
						<samp>
						    <textarea id="<?= $qtype; ?>" class="sprql_textarea" name="sparql"><?= $qstring; ?></textarea>
						</samp>
					    </div>
					<?php else: ?>
				            <div data-content="<?= $counter; ?>" class="content">
						<samp>
						    <textarea id="<?= $qtype; ?>" class="sprql_textarea" name="sentence"><?= $qstring; ?></textarea>
						</samp>
					    </div>
					<?php endif; ?>
                                  <?php endforeach; ?>
				</div>
				<!-- /tabs -->
			      <?php endif; ?>
                           
			   <?php else: ?>
				<samp>
				      <textarea id="notype" class="sprql_textarea" name="sparql"></textarea>
			        </samp>
			   <?php endif; ?>
		<!-------------------->
                        <input type="hidden" name="format" value="json" />
                        <button id="send_qsentence" type="button" class="btn btn-default btn-sm">
                            <span class="glyphicon glyphicon-filter"></span> send query to web services
                        </button>
		<!-------------------->
		</fieldset>
	    </form>
        </div>
<!------------------------_______SPARQL RESULT________________------------------------------------> 
        <div class="clear"></div>
	<br />
        <div id="qresults">
	    <legend>SPARQL result:</legend>
            <div class="qresult_left">
		    <?php
		        if(isset($resultData) && count($resultData["display"]) > 0){
		            if(isset($data["fst"])){
				foreach($resultData["display"] as $key => $value){
				    echo $key . "<br />";
				    foreach($value as $k => $v){
					echo "<a href=" . $v . ">" . $v . "</a><br />";
				    }
				}
			    }
			    else if(isset($data["scnd"])){
				foreach($resultData["display"] as $key => $value){
				    echo $key . "<br />";
				    /*print_r($value);*/
				    foreach($value as $tyyp => $items){
		                        if($tyyp == "loc")
					    echo "<h4>locations:</h4>";
		                        else if($tyyp == "org")
					    echo "<h4>organizations:</h4>";
		                        else
					    echo "<h4>" . $tyyp . ":</h4>";
					foreach($items as $k => $v){
					    echo "<div class='items'>" . $v . "</div>";
					}
				    }

				}
			    }
			}
			else{
			    echo "{}";
			}
		    ?>
            </div>
            <div class="qresult_right" id="qresult_formats">
                <h4 id="caption">web services resulting in formats json, rdf/xml:</h4>
                <div>webservice takes in SPARQL query sentence as POST parameter "sparql" value</div>
                <div class="format_items" id="format_items">
                    <div class="format_item" id="service_people">
			<h4>people:</h4>
                        <form method="post">
                            <textarea id="input_people" class="input_q" name="sparql"></textarea>
			    <br />
                            <button class="btn btn-danger btn-sm" type="submit" formaction="structures/json/">get JSON response</button>
                            <button class="btn btn-danger btn-sm" type="submit" formaction="structures/xml/">get RDF/XML response</button>
                        </form>
                   </div>
                    <div class="format_item" id="service_org">
			<h4>organizations:</h4>
                        <form method="post">
                            <textarea id="input_org" class="input_q" name="sparql"></textarea>
			    <br />
                            <button class="btn btn-danger btn-sm" type="submit" formaction="structures/json/">get JSON response</button>
                            <button class="btn btn-danger btn-sm" type="submit" formaction="structures/xml/">get RDF/XML response</button>
                        </form>
                   </div>
                    <div class="format_item" id="service_loc">
			<h4>locations:</h4>
                        <form method="post">
                            <textarea id="input_loc" class="input_q" name="sparql"></textarea>
			    <br />
                            <button class="btn btn-danger btn-sm" type="submit" formaction="structures/json/">get JSON response</button>
                            <button class="btn btn-danger btn-sm" type="submit" formaction="structures/xml/">get RDF/XML response</button>
                        </form>
                   </div>
                </div>
                    <div class="format_item_notype" id="service_notype">
                        <form method="post">
                            <textarea id="input_notype" class="input_q" name="sparql"></textarea>
			    <br />
                            <button class="btn btn-danger btn-sm" type="submit" formaction="structures/json/">get JSON response</button>
                            <button class="btn btn-danger btn-sm" type="submit" formaction="structures/xml/">get RDF/XML response</button>
                        </form>
                   </div>
                  <!--
                    <a href="http://www.w3.org/TR/rdf-testcases/#ntriples"><h4>ntriples</h4></a>
                    <div class="format_item" id="format_ntriples"></div>

                    <a href="http://www.w3.org/2007/11/21-turtle"><h4>turtle</h4></a>
                    <div class="format_item" id="format_turtle"></div>

                    <a href="https://www.w3.org/2007/11/21-n3"><h4>n3</h4></a>
                    <div class="format_item" id="format_n3"></div>
                   -->
	    </div>

            <div class="clear"></div>

        </div>
        <br /><br /><br />
    </div>
    </body>
</html>
