

console.log("this uploadscript.js")
$(document).ready( function () {
    console.log("this uploadscript.js ready")
    showPreviewImage();
});

function showPreviewImage() {
    $("#ImageMedia").change(function () {
        console.log("begin ....")
        if (typeof (FileReader) != "undefined") {
            console.log("image change")
            if ($(this)[0].files && $(this)[0].files[0]) {
                var file = $(this)[0].files[0];
                var reader = new FileReader();
                reader.onload = function(e){
                    var img = $("#cropbox");
                    img.attr("src", e.target.result);
                }
                reader.readAsDataURL(file);
            }
        } else {
            alert("This browser does not support HTML5 FileReader.");
        }
    });
}
