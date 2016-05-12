$(document).ready(function() {
    //$("#notifycation_alert").show();
    //$(".extr_form").hide();
/**/
    $( ".extr_form" ).submit(function( event ) {
        $("#notifycation_alert").show();
        var logfilename = $(this).find("input:first[type='hidden']").val();

        mess = "<span class='tanap'>" +tanapaev() + "</span> Notifycation: <br>RDFizing of <span class='fname'>" + logfilename + "</span>. <br>This may take several hours.";
        $("#notifycation_alert").append(mess);
        $("input").hide();
        //event.preventDefault();
    });

    $( "#simulate_update" ).submit(function( event ) {
        //window.alert("BB");
        $("#notifycation_alert_simulate").show();
        mess = "<span class='tanap'>" +tanapaev() + "</span> Notifycation: <br>Updating RDF-files and datasets. <br>This may take several hours.";
        $("#notifycation_alert_simulate").append(mess);
        $("input").hide();
        //event.preventDefault();
    });


});



function tanapaev(){
    var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();
        var hour = today.getHours();
        var minute = today.getMinutes();
        var sec = today.getSeconds();

	if(dd<10) {
	    dd='0'+dd
	} 

	if(mm<10) {
	    mm='0'+mm
	} 

	today = mm+'/'+dd+'/'+yyyy + " " + hour + ":" + minute + ":" + sec ;
	return (today);
}
