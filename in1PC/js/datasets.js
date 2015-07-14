$(document).ready(function() {
    //$("#notifycation_alert").show();
    //$(".extr_form").hide();
/**/
    $( ".pagenmbrs" ).click(function( event ) {
        var id = $(this).attr('id');
        var host = $(location).attr('host');
        var pathname = $(location).attr('pathname');
        var redirect = host + pathname + "?page=" + id;
        window.location.href = "http://"+redirect;
        //window.alert(id + " " + base);
        //event.preventDefault();
    });
    $( ".pagenmbrs" ).keydown(function(e){
        window.alert(e);
    });

   $( ".remote_file_type_species" ).click(function( event ) {
        var id = $(this).attr('id');
        var host = $(location).attr('host');
        var pathname = $(location).attr('pathname');
        var redirect = host + pathname + "?type=" + id;
        window.location.href = "http://"+redirect;
    })


    $( "input.host_search_btn" ).click(function( event ) {
        var hostname = $("input#host_search_input").val();
        //window.alert(hostname);
        var host = $(location).attr('host');
        var pathname = $(location).attr('pathname');
        var redirect = host + pathname + "?host=" + hostname;
        window.location.href = "http://"+redirect;
        //event.preventDefault();
    });

});
