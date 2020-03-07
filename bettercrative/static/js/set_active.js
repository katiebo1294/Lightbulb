//sets the value of a quiz to active and resets the section of the page, later we should change this refresh portion however for now it works.
function set_active(url, name, classroom_id) {
    console.log("setting active...");
    $.ajax({
        type: "GET",
        data: {'name': name, 'classroom_id' : classroom_id},
        url: url,
        error: function(statusText) {
            console.log(fail);
            alert(statusText);
            console.log(statusText);
        },
        success: function() {
            console.log("success");
            refresh("#body");
        }
    });
}

function remove_active(url, classroom_id) {
    console.log("remove active...");
    $.ajax({
        type: "GET",
        data: {'classroom_id' : classroom_id},
        url: url,
        error: function(statusText) {
            console.log(fail);
            alert(statusText);
            console.log(statusText);
        },
        success: function() {
            console.log("success");
            refresh("#body");
        }
    });
}