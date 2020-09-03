
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
    document.getElementById("modalPopUp").style.display = "none";
}

// create Classroom
function createClassroomPopup() {
    modal = document.getElementById("modalPopUpForm");
    modalForm = document.getElementById("modalClass");
    modalText = document.getElementById("modalTextForm")
    modalText.innerHTML = "Create Classroom";
    modal.style.display = "block";
    modalForm.style.display = "block";
}

function unset_and_edit(quiz_id){
    var quiz = document.getElementById('default-'+quiz_id);
    quiz.classList.add('noshow');
    quiz = document.getElementById('unset-and-edit-'+quiz_id);
    quiz.classList.remove('noshow');
    quiz.classList.add('show');
}

function unset_and_edit_confirm(quiz_id){
    event.preventDefault();
    $.ajax({
        type: "POST",
        data: {'quiz_id': quiz_id},
        url: '/classroom/unset_and_edit',
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
           
            
            window.location.replace('/quiz/'+quiz_id);
               
            
        }
    });
}


$('#quiz_active_modal').on('hidden.bs.modal', function (e) {
    location.reload();
    
})