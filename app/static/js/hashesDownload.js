$('#downloadBtn').on('click', function() {
    var data = {'hashWord': []};
    console.log(data['hashWord']);

    $('td').each(function() {
        data.hashWord.push($(this).text().trim());
    });

    console.log(data.hashWord)
    $('<a />', {
        "download": "hashes.json",
        "href": "data:application/json;charset=utf-8," +
            encodeURIComponent(JSON.stringify(data)),
    }).appendTo('body').click(function(){
        $(this).remove()
    })[0].click()
})
