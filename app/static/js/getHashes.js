var selected = []


$(document).on("click", 'tr.word', function selectWord(){
    if ($(this).hasClass('selected')) {
        $(this).removeClass('selected');
        var index = selected.indexOf($(this).text().trim());
        selected.splice(index, 1);
    } else {
        $(this).addClass('selected');
        selected.push($(this).text().trim());
    }

    if (selected.length != 0) {
        $('#getHashesBtn').removeClass('disabled');
    } else {
        $('#getHashesBtn').addClass('disabled');
    }
});


$('#getHashesBtn').on('click', function sendWords() {
    if (!$(this).hasClass('disabled')) {

        $(this).addClass('disabled');
        $('tr.selected').each(function() {
            $(this).removeClass('selected');
        });

    $.ajax({
        type: 'POST',
        url: '/getHashes',
        data: {'words': JSON.stringify(selected),
               'algorithm': $('#hashers :selected').text()},
        error: function(error) {
            console.log(error);
        }
    }).done(function(data) {
        if (data.status === 1) {

            selected = []

            $("#resultGetHashes").hide(1000)
              .removeClass()
              .addClass("alert alert-success results")
              .text("Hashing completed!")
              .show(500)
              .slideUp(1500);
        }
    })
}
})
