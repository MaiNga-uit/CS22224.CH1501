$(document).ready( function () {
    $('#prePage').hide();
    $('#nextPage').hide();
    $('#prePage').click(function(){ onPageChange(-1); return false; });
    $('#nextPage').click(function(){ onPageChange(1); return false; });
    loadImage();
});


function loadImage(page) {
    const urlParams = new URLSearchParams(decodeURIComponent(window.location.search));
    var page = urlParams.get('page');
    if (page == null || page.length === 0) {
        page = '1';
    }

    var pageNumber = parseInt(page, 10);
    if (pageNumber > 1) {
        console.log("show pre page");
        $('#prePage').show();
    }

    console.log("query page = " + pageNumber);

    $.ajax({
        url: '/api/datasets?page=' + pageNumber,
    }).done(function(msg) {
        if (msg === undefined) {
            return
        }

        if (msg.total !== undefined) {
            console.log("Set page info: ", msg)
            $('#pageInfo').text(`Trang ${msg.page}, hình từ ${msg.indexFrom} đến ${msg.indexTo} trên ${msg.total} hình`)
        }

        if (msg.hasNext) {
            $('#nextPage').show();
        }

        if (msg.data === undefined) {
            return
        }

        for (imageName of msg.data) {
            var aTag = $("<a />");
            aTag.attr("href", 'search.html?id=' + imageName);

            var imgTag = $("<img />");
            imgTag.attr("class", "small-square-image");
            imgTag.attr("src", 'dataset/' + imageName);

            aTag.append(imgTag);

            $('#gridContent').append(aTag);
        }
    });
}

function onPageChange(added) {
    const urlParams = new URLSearchParams(decodeURIComponent(window.location.search));
    var page = urlParams.get('page');
    if (page == null || page.length === 0) {
        page = '1'
    }

    var pageNumber = parseInt(page, 10);

    pageNumber += added;
    if (pageNumber <= 0) {
        return;
    }

    urlParams.set('page', pageNumber);
    fullUrl = window.location.origin + window.location.pathname + '?' + urlParams.toString()
    console.log("Go to: " + fullUrl)
    window.location.href = fullUrl
}