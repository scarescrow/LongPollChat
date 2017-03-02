$(function() {
    
    function doPoll() {
        payload = {
            'user': username,
            'sender': receiver
        }
        $.get("/redischat/getpendingmessages",
            payload, 
            function(response) {
            response = $.parseJSON(response);
            messages = response['messages'];
            for (var i = 0; i < messages.length; i ++) {
                var message = messages[i];
                $('#messages').append("<li>" + message.date + ">" + 
                    message.sender + " - " + message.body + "</li>")
            }
            setTimeout(doPoll, 5000);
        });
    }
    // Async function to start listener if not started
    $.get("/redischat/startclient", function(response) {
        console.log(response);
    });

    doPoll();

    $('#send').click(function() {
        var message = $('#input-msg').val();
        if (message.length === 0) {
            alert("Please enter a message");
            return false;
        }
        var payload = {
            'sender': username,
            'receiver': receiver,
            'message': message
        }
        $.get("/redischat/sendmessage", payload, function(response) {
            console.log(response);
            response = $.parseJSON(response);
            var time = response['time']
            $('#messages').append("<li>" + time + ">" + 
                    username + " - " + message + "</li>");
            $('#input-msg').val("");
        });
        return false;
    });


});