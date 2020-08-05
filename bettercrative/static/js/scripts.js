$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked hamburger");
});

$(window).scroll(function () {
    smoothnav = document.getElementsByClassName("navbar")[0];
    if ($(document).scrollTop() > 30) {
        $(smoothnav).addClass('affix').animate();
    } else {
        $(smoothnav).removeClass('affix').animate();
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

function openLatexAlert() {
    modal = document.getElementById("modalPopUp");
    modalText = document.getElementById("modalText");
    modalTitle = document.getElementById("modalTitle");
    modalButton = document.getElementById("modalButton");
    cancelButton = document.getElementById("cancelButton");
    modalTitle.innerHTML = "Did you know?";
    modalText.innerHTML = "We have Latex Integration! </br> Simply type anything in Latex into your question or answer, and we will convert it for you!";
    modalButton.innerHTML = "Got it!";
    modalButton.onclick = function() {modal.style.display="none"};
    cancelButton.style.display = "none";
    modal.style.display = "block";
}