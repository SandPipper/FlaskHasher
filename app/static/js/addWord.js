$('#addWordBtn').on('click', function() {
    $.ajax({
        type: 'POST',
        url: '/addWord',
        data: $('#addWord').serialize(),
        error: function(error) {
            console.log(error);
        }
    }).done(function(data) {
        if (data.status === 1) {

            var output = '<tr class="word"><td>' + data.message + '</td></tr>';
            $('table').append(output);

            $("#resultAddWord").hide(1000)
              .removeClass()
              .addClass("alert alert-success results")
              .text("Word is successfuly added!")
              .show(500)
              .slideUp(1500);

        } else if (data.status === 0) {
            $("#resultAddWord").hide(1000)
              .addClass("alert alert-danger results")
              .text(data.message)
              .show(300)
              .slideUp(2000);

        }
        $('#addWord')[0].reset();
    })
    })
