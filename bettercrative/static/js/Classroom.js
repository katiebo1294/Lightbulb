// remove Classroom
function removeClassroomPopup(url, c_id) {
    modal = document.getElementById("modalPopUp");
    modalText = document.getElementById("modalText")
    modalButton = document.getElementById("modalButton");
    modalText.innerHTML = "Are you sure that you want to delete this classroom??";
    modalButton.onclick = function() {removeClassroom(url,c_id)};
    modal.style.display = "block";
}

function removeClassroom(url, c_id) {
    $.ajax({
        type: "GET",
        data: {'classroom_id': c_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#classroomListing");
        }
    });
    document.getElementById("modalPopUp").style.display = "none";;
}

// create Classroom
function createClassroomPopup() {
    document.getElementById("modalQuiz").style.display = "none";
    modal = document.getElementById("modalPopUpForm");
    modalForm = document.getElementById("modalClass");
    modalText = document.getElementById("modalTextForm")
    modalText.innerHTML = "Create Classroom";
    modal.style.display = "block";
    modalForm.style.display = "block";
}
