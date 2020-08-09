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

// this colors the current page's link in the navbar green
currentLinks = document.querySelectorAll('a[href="'+ document.URL.substr(document.URL.lastIndexOf("/")) +'"].nav-link');
console.log(currentLinks);
    currentLinks.forEach(function(link) {
        link.className += ' current-page';
        var newSpan = document.createElement('span');
        newSpan.className += 'sr-only';
        newSpan.innerHTML = "(current)";
        link.appendChild(newSpan);
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
    modalText.innerHTML = "We have LaTeX Integration! </br> Simply type anything in LaTeX into your question or answer, and we will convert it for you!";
    modalButton.innerHTML = "Got it!";
    modalButton.onclick = function() {modal.style.display="none"};
    cancelButton.style.display = "none";
    modal.style.display = "block";
}

function showAccountEditForm() {
    document.getElementById("account-info-container").style.display = "none";
    document.getElementById("user-stats").style.display = "none";
    document.getElementById("account-form").style.display = "block";
}

function sortList(element) {
    // get decendant that has <i>
    var itag = element.getElementsByTagName("i")[0];
    var direction;
    // changes the direction of ordering 
    if(itag.classList.contains('sort-descending')) {
        itag.className = ('fas fa-arrow-up sort-ascending');
        direction = false;
    } else {
        itag.className = ('fas fa-arrow-down sort-descending');
        direction = true;
    }

    // Send a GET request to reload the page TODO doesn't work
    console.log("success sort on " + element.id + " " + direction);
    $.ajax({
        type: "GET",
        data: {
            sort_on: element.id, 
            sort_direction: direction
        },
        url: document.URL,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            console.log("success sort on " + element.id + " " + direction);
            // $("#" + type + "-data").load(" #" + type + "-data > *");
        }
    });
}