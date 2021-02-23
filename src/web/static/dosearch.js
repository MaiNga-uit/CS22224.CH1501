$(document).ready( function () {
    $('#primarycontent').hide();
    callDoSearchAPI();
});

function callDoSearchAPI() {
    console.log("call do search api: " + window.location.search);

    $.ajax({
        url: '/api/dosearch' + window.location.search,
    }).done(function(msg) {
        $('#loading').hide();
        $('#primarycontent').show();
        
        if (msg === undefined) {
            return
        }

        if (msg.searchImageInfo === undefined) {
            return
        }

        console.log("Response msg: ", msg);
        var searchImageInfo = msg.searchImageInfo;
        console.log("searchImageInfo: ", searchImageInfo);

        //Append searchImageInfo to UI
        var divImageSearch = $("<div />");
        divImageSearch.attr("class", 'searchImage');
        var divImage = $("<div />");
        divImage.attr("class", 'image');

        var aTag = $("<a />");
        aTag.attr("href", 'search.html?id=' + searchImageInfo.id);
        var imgTag = $("<img />");
        imgTag.attr("class", "small-square-image");
        imgTag.attr("src", 'dataset/' + searchImageInfo.id + '?' + searchImageInfo.rect);
        aTag.append(imgTag);

        divImage.append(aTag);
        divImageSearch.append(divImage)
        $('#searchImageDiv').append(divImageSearch);


        if (msg.results === undefined) {
            return
        }

        // Append results to UI
        for (let [index, imageInfo] of msg.results.entries()) {
            if (imageInfo.id === undefined) {
                continue
            }

            var divImageresult = $("<div />");
            divImageresult.attr("class", 'imageresult');

            //Append divNumber
            var divNumber = $("<div />");
            divNumber.attr("class", 'res_num');
            divNumber.text(index + 1)
            divImageresult.append(divNumber)

            //Append divImage
            var divImage = $("<div />");
            divImage.attr("class", 'image');

            var aTag = $("<a />");
            aTag.attr("href", 'search.html?id=' + imageInfo.id);
            var imgTag = $("<img />");
            imgTag.attr("class", "small-square-image");
            imgTag.attr("src", 'dataset/' + imageInfo.id);
            aTag.append(imgTag);

            divImage.append(aTag);
            divImageresult.append(divImage)

            //Append info detail
            var divInfo = $("<div />");
            divInfo.attr("class", 'info');
            var textInfo = `ID: ${imageInfo.id} <br/>`;
            divInfo.html(textInfo);
            divImageresult.append(divInfo);

            //Append to resultList
            $('#resultList').append(divImageresult);
        }
    });
}