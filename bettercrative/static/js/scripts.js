$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked hamburger");
    $("#navlistcontents").toggleClass("show_list");
    $("#navlistcontents").fadeIn();
});

$(window).scroll(function () {
    if ($(document).scrollTop() > 30) {
        $('.nav').addClass('affix');
    } else {
        $('.nav').removeClass('affix');
    }
});

function dropDown() {
    var x = document.getElementById("navlistofcontents");
    if (x.className === "listofcontents") {
        x.className += " responsive ";
    }
    else {
        x.className = "listofcontents";
    }
}

function goBack() {
    window.history.back();
    console.log("Going back to previous page");
}

setTimeout(function () {
    $(".alert").fadeTo(300, 0).slideUp(300, function () {
        $(this).remove();
    });
}, 1500);
