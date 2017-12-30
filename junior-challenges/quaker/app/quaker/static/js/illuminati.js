$(document).ready(function() {
    var eye = $('#the-eye'); 
    $('#circle').attr('coords', ''+eye.width()/2+','+eye.height()/2+','+eye.width() / 2 * 0.15);

    $("#form").submit( function(form) {
        console.log(this);
        var xml = "<illuminato>";
        xml += "<details>" + this.details.value + "</details>";
        xml += "<video>" + this.video.value + "</video>";
        xml += "</illuminato>";

        $("<input />").attr("type", "hidden")
            .attr("name", "xml")
            .attr("value", xml)
            .appendTo(this)

        return true;
    });

    $("#snd")[0].volume = .5;


    setTimeout(function() {
        $("#illu").find("iframe").prop("src", function(){
            return $(this).data("src");
        });
        $("#illu").fadeIn(4000);
    }, 10000);
});

