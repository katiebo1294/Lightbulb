//sets the value of a quiz to active and resets the section of the page, later we should change this refresh portion however for now it works.
function set_active(url, q_id) {
    $.ajax({
        type: "GET",
        data: {'quiz_id': q_id, 'classroom_id' : classroom_id},
        url: url,
        error: function(statusText) {
            alert(statusText);
            console.log(statusText);
        },
        success: function() {
            refresh("#questionNav");
        }
    });
}