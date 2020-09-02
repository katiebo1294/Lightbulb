// remove Classroom
function removeClassroomPopup(url, c_id) {
    modal = document.getElementById("modalPopUp");
    modalText = document.getElementById("modalText");
    modalButton = document.getElementById("modalButton");
    modalText.innerHTML = "Are you sure that you want to delete this classroom??";
    modalButton.onclick = function() {removeClassroom(url,c_id)};
    modal.style.style.display = "block";
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
    document.getElementById("modalPopUp").style.display = "none";
}

// create Classroom
function createClassroomPopup() {
    modal = document.getElementById("modalPopUpForm");
    modalForm = document.getElementById("modalClass");
    modalText = document.getElementById("modalTextForm")
    modalText.innerHTML = "Create Classroom";
    modal.style.style.display = "block";
    modalForm.style.display = "block";
}

/**
 * Description:
    shows the classroom edit form
 * Param:
    classroom_id:
        id of that classroom
 * Return:
    n/a
 */
function showEditClassroom(classroom_id){
    //Getting the classroom we want to edit
    document.getElementById("classroom-" + classroom_id).style.display = "none";
    document.getElementById("classroom-form-" + classroom_id).style.display = "inline-block";
}

function cancelEditClassroom(classroom_id){
    document.getElementById("classroom-" + classroom_id).style.display = "inline-block";
    document.getElementById("classroom-form-" + classroom_id).style.display = "none";
}
