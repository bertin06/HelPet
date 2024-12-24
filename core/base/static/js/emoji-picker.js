$(document).ready(function() {
    $('.emoji').click(function() {
        var emoji = $(this).text();
        $('#chat-message-input').val(function(index, value) {
            return value + emoji;
        });
    });
});