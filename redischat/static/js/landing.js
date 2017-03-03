$(function() {
    // Async function to start listener if not started
    $.get("/redischat/startclient", function(response) {
        console.log(response);
    });
});