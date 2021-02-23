$(document).ready( function () {
    getImageFromURL();
});

function getImageFromURL() {
    const urlParams = new URLSearchParams(decodeURIComponent(window.location.search));
    const imageId = urlParams.get('id');

    console.log("imageId = " + imageId)
    if (imageId == null || imageId.length === 0) {
        return;
    }

    var img = $("#cropbox");
    if (img == null || img == "undefined") {
        return;
    }

    img.attr("src", 'dataset/'+imageId);
    URLBASE += imageId;
}