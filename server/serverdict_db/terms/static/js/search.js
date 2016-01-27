$(document).ready(function() {
    $('#submit_btn').click(function() {
        $.get("/search",
            {
                q: $('#query_text_edit').text()
            }, function() {
                //alert($('#query_text_edit').text());
            }
        );
    });
});