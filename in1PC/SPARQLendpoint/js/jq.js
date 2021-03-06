$(document).ready(function() {
    fillWebserviceForm();
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

   
    $( "button#send_qsentence" ).click(function() {
        fillWebserviceForm();
    });

    $( "#sprqlform" ).
	submit(function( event ) {
                fillWebserviceForm();
		event.preventDefault();
    });

});

function fillWebserviceForm(){
     //input_q "input_q"
     var sparql_array = {};
     $( "textarea.sprql_textarea" ).each(function( index ) {
	    var sparql = ($(this).html());//encodeURIComponent($(this).html());//
            var areaid = $(this).attr('id');
            //console.log("id", areaid);
            sparql_array[areaid] =  htmspecials(sparql);
     });

    

     //empty webservices and meke them  invisible
     $( "textarea.input_q" ).each(function( index ) {
	    $(this).val("");
     });
     $( "div#format_item" ).each(function( index ) {
	    $(this).fadeOut( 200 );
     });

     var arrayIsEmpty = 1;
     for (var i in sparql_array) {
	if(sparql_array[i] != ""){
	    arrayIsEmpty = 0;
	}
     }
     console.log(sparql_array);
         
    if(!arrayIsEmpty){
        $( "div#qresult_formats" ).show().fadeOut( 200 ).fadeIn( 200 );
        $("div#format_items").removeClass("format_items").addClass("format_items_visible");
    }
     
    if(!arrayIsEmpty){
	if(sparql_array["people"] != undefined){
           if(sparql_array["people"] != ""){
               $("div#service_people").fadeIn( 200 );
               $( "textarea#input_people" ).val(sparql_array["people"]);
           }
	    
	}
        else{
            $("div#service_people").hide().fadeOut( 200 );
	}
	if(sparql_array["organizations"] != undefined){
           if(sparql_array["organizations"] != ""){
               $("div#service_org").fadeIn( 200 );
               $( "textarea#input_org" ).val(sparql_array["organizations"]);
           }
	    
	}
        else{
            $("div#service_org").fadeOut( 200 );
	}
	if(sparql_array["locations"] != undefined){
           if(sparql_array["locations"] != ""){
               $("div#service_loc").fadeIn( 200 );
               $( "textarea#input_loc" ).val(sparql_array["locations"]);
           }
	    
	}
        else{
            $("div#service_loc").fadeOut( 200 );
	}
	if(sparql_array["notype"] != undefined){
           if(sparql_array["notype"] != ""){
               $("div#service_notype").fadeIn( 200 );
               $( "textarea#input_notype" ).val(sparql_array["notype"]);
           }
	   else{
	       $("div#service_notype").show().fadeIn( 200 );
	   }
	    
	}
        else{
            $("div#service_notype").fadeOut( 200 );
	}
    }
    else{
        $("div#service_notype").show().fadeIn( 200 ).addClass("format_items_visible");
    }
}

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

//stackoverflow.com/questions/1248849/converting-sanitised-html-back-to-displayable-html
function htmspecials(sparql) {
    var ret = sparql.replace(/&gt;/g, '>');
    ret = ret.replace(/&lt;/g, '<');
    ret = ret.replace(/&quot;/g, '"');
    ret = ret.replace(/&apos;/g, "'");
    ret = ret.replace(/&amp;/g, '&');
    return ret;
};
