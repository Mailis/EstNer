$(document).ready(function() {

    
    //var sparql_ = encodeURI($( "textarea.sprql_textarea" ).html());
    //if(sparql_ != "")
        fillStructuresDiv();
    /*
    var stored_sparql = localStorage.getItem("stored_sparql");
    if(stored_sparql != null){
        fillStructuresDiv(stored_sparql);
    }
    */
    var radiotyypValue = $('input[name=tyypradio]:checked').val();
    showInputTyyp(radiotyypValue);
    $("input[name=tyypradio]:radio").change(function () {
	$( ".selectedtyyp_visible" ).removeClass('selectedtyyp_visible').addClass('selectedtyyp');
	var radiotyypValue = this.value;
	showInputTyyp(radiotyypValue);
        //empty all inputs
        $("input:text.fstcol").val("");
        //remove error notes
        removeErrorNotes();
    });

    $( "#sprqlform" ).
	submit(function( event ) {
		
                /*localStorage.setItem("stored_sparql", sparql);*/
		fillStructuresDiv();

		event.preventDefault();
	});


    //processed log files' stat
     $.get("displayStatistics.php")
	     .done(function( data ) {
              $("div.stat_waiter").html(data);
        });
    


    //fill nr of lines of log file
    $("td.nroflines").each(function() {
        $tdcell = $(this);
        fid = $tdcell.attr('id');
        logfilename = fid.replace("_-", ".");
        
        $.get( "getNumberOfLines.php", { id: fid, filename: logfilename} )
	     .done(function( data ) {
              var obj = jQuery.parseJSON(data);
              for(i in obj){
                   $("td#" +i).html(obj[i]);
              }
        }, "json");
        
    });

   
});


function showInputTyyp(radiotyypValue){
    $inputEl = $( "#" + radiotyypValue + "_input" );
    $inputEl.removeClass('selectedtyyp');
    $inputEl.addClass('selectedtyyp_visible');
}

function removeErrorNotes(){
        $("div#error").removeClass('hasError');
        $("div#error").addClass('noError');
}


$(function () {
    
      $('[data-tab]').on('click', function (e) {
        $(this)
          .addClass('active')
          .siblings('[data-tab]')
          .removeClass('active')
          .siblings('[data-content=' + $(this).data('tab') + ']')
          .addClass('active')
          .siblings('[data-content]')
          .removeClass('active');
        e.preventDefault();
      });
      
    });



function fillStructuresDiv(sparql){

     var sparql_array = {};
     $( "textarea.sprql_textarea" ).each(function( index ) {
	    var sparql = encodeURI($(this).html());
            var areaid = $(this).attr('id');
            //console.log("id", areaid);
            sparql_array[areaid] = sparql;
     });
     //console.log(sparql_array);
     var arrayIsEmpty = 1;
     for (var i in sparql_array) {
	if(sparql_array[i] != ""){
	    arrayIsEmpty = 0;
	}
     }
         
    if(!arrayIsEmpty){
        $( "div#qresult_formats" ).show().fadeOut( 200 ).fadeIn( 200 );
        $("div#format_items").removeClass("format_items").addClass("format_items_visible");
    }
    $( "div#format_json" ).html("");
    $( "div#format_xml" ).html("");

    if(!arrayIsEmpty){
	for (var i in sparql_array) {
	    if(sparql_array[i] != ""){
		if(i != "")
                	var newspan = $("<span />", {text : i, class : 'objtype'});

                var newLink = $("<a />", {
				    class : "a_link",
				    name : "link",
				    href : "structures/json/?sparql=" + sparql_array[i],
				    text : "structures/json/?sparql=" + sparql_array[i]
				});
                if(i != ""){
			$( "div#format_json" ).append(newspan);
			$( "div#format_json" ).append("<br />");
		}
		$( "div#format_json" ).append(newLink);
	    }
         }

	for (var i in sparql_array) {
	    if(sparql_array[i] != ""){
		if(i != "")
                    var newspan = $("<span />", {text : i, class : 'objtype'});

		var newLink = $("<a />", {
				    class : "a_link",
				    name : "link",
				    href : "structures/xml/?sparql=" + sparql_array[i],
				    text : "structures/xml/?sparql=" + sparql_array[i]
				});
                if(i != ""){
			$( "div#format_xml" ).append(newspan);
			$( "div#format_xml" ).append("<br />");
		}
		$( "div#format_xml" ).append(newLink);
	    }
         }
    }

/*
		newLink = $("<a />", {
				    id : "a_ntriples",
				    name : "link",
				    href : "structures/ntriples/?sparql=" + sparql,
				    text : "structures/ntriples/?sparql=" + sparql
				});
		$( "div#format_ntriples" ).html(newLink);

		newLink = $("<a />", {
				    id : "a_turtle",
				    name : "link",
				    href : "structures/turtle/?sparql=" + sparql,
				    text : "structures/turtle/?sparql=" + sparql
				});
		$( "div#format_turtle" ).html(newLink);

		newLink = $("<a />", {
				    id : "a_n3",
				    name : "link",
				    href : "structures/n3/?sparql=" + sparql,
				    text : "structures/n3/?sparql=" + sparql
				});
		$( "div#format_n3" ).html(newLink);
*/
}

function tog(thisid){
   var elem = document.getElementById(thisid);
   nextSibling = elem.nextSibling;
   nextSibling.style.display = (nextSibling.style.display == 'block' ? 'none' : 'block' );  
}
