
// remove Classroom
function removeClassroomPopup(url, c_id) {
    modal = document.getElementById("modalPopUp");
    modalText = document.getElementById("modalText");
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
function show_unset(quiz_id){
    var quiz = document.getElementById('default-'+quiz_id);
    quiz.classList.add('noshow');
    quiz = document.getElementById('unset-'+quiz_id);
    quiz.classList.remove('noshow');
    quiz.classList.add('show');
    
    //listener for modal close
    $('#document').ready(function(){
        $('#quiz_active_modal').on('hidden.bs.modal', function(){
            console.log('refreshing the modal content')
            const modal_content = document.getElementById('unset-'+quiz_id);
            modal_content.classList.remove('show');
            modal_content.classList.add('noshow');
            const default_modal = document.getElementById('default-'+quiz_id);
            default_modal.classList.remove('noshow');
            default_modal.classList.add('show');
        });
    })
}

function show_unset_and_edit(quiz_id){
    var quiz = document.getElementById('default-'+quiz_id);
    quiz.classList.add('noshow');
    quiz = document.getElementById('unset-and-edit-'+quiz_id);
    quiz.classList.remove('noshow');
    quiz.classList.add('show');
    
    //listener for modal close
    $('#document').ready(function(){
        $('#quiz_active_modal').on('hidden.bs.modal', function(){
            console.log('refreshing the modal content')
            const modal_content = document.getElementById('unset-and-edit-'+quiz_id);
            modal_content.classList.remove('show');
            modal_content.classList.add('noshow');
            const default_modal = document.getElementById('default-'+quiz_id);
            default_modal.classList.remove('noshow');
            default_modal.classList.add('show');
        });
    })
}
function unset_confirm(quiz_id, classroom_id){
    event.preventDefault();
    $.ajax({
        type: "POST",
        data: {'quiz_id': quiz_id, 'classroom_id': classroom_id},
        url: '/classroom/unset',
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
           
            
            location.reload();
               
            
        }
    });
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

function toggleEditClassroomTitle() {
    $("#classroom-title-display").toggle();
    $("#classroom-title-edit").toggle();
}

function resizeInput() {
    $(this).attr('size', $(this).val().length);
}

$("#classroomname-content-3").keydown(resizeInput).each(resizeInput);


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

// for setting/unsetting quizzes active
$("button[id^='set-active-']").click(function () {
    var classroom_id = this.id.slice(14);
    var quiz_id = this.id.slice(lastIndexOf('-'));
    $.ajax({
        type: 'GET',
        data: { 'classroom_id': classroom_id },
        url: '/classroom/' + classroom_id + '/set_active',
        error: function(response) {
            console.log(response.statusText);
        },
        success: function() {
            window.location.reload();
        }
    });
});

$("button[id^='remove-active-']").click(function () {
    var classroom_id = this.id.slice(14);
    $.ajax({
        type: 'GET',
        data: { 'classroom_id': classroom_id },
        url: '/classroom/' + classroom_id + '/remove_active',
        error: function(response) {
            console.log(response.statusText);
        },
        success: function() {
            window.location.reload();
        }
    });
});
