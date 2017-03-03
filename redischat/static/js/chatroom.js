$(function() {
    
    function doPoll() {
        payload = {
            'user': username,
            'sender': receiver
        }
        $.ajax({
            url: "/redischat/getpendingmessages",
            data: payload,
            timeout: 30000,
            method: 'get',
            success: function(response) {
                response = $.parseJSON(response);
                messages = response['messages'];
                for (var i = 0; i < messages.length; i ++) {
                    var message = messages[i];
                    $('#messages').append("<li>" + message.date + ">" + 
                        message.sender + " - " + message.body + "</li>")
                }
                setTimeout(doPoll, 1000);
            }, 
            error: function() {
                setTimeout(doPoll, 3000)
            }
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
        $('#input-msg').val("");
        $.get("/redischat/sendmessage", payload, function(response) {
            console.log(response);
            response = $.parseJSON(response);
            var time = response['time']
            $('#messages').append("<li>" + time + ">" + 
                    username + " - " + message + "</li>");
        });
        return false;
    });


});