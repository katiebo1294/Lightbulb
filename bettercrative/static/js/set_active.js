//sets the value of a quiz to active and resets the section of the page, later we should change this refresh portion however for now it works.
function set_active(url, quiz_id, classroom_id) {
    console.log("setting active...");
    $.ajax({
        type: "GET",
        data: {'quiz_id': quiz_id, 'classroom_id' : classroom_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            console.log("success");

            refresh('#question');
        }
    });
}

function remove_active(url, classroom_id) {
    console.log("remove active...");
    $.ajax({
        type: "GET",
        data: {'classroom_id' : classroom_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            console.log("success");
            refresh("#quizzes-"+classroom_id);

        }
    });
}

