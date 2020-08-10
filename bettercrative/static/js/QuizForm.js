function addQuestion(url, q_id) {
    
    $.ajax({
        type: "GET",
        data: {'quiz_id': q_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#questionView");
        }
    });
}

function addAnswer(url, q_id, index) {
    $.ajax({
        type: "GET",
        data: {'question_id': q_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#question-edit-" + index);
        }
    });
}
// remove Question
function removeQuestionPopup(url, q_id) {
    modal = document.getElementById("modalPopUp");
    modalText = document.getElementById("modalText");
    modalButton = document.getElementById("modalButton");
    modalText.innerHTML = "Are you sure that you want to delete this question?";
    modalButton.onclick = function() {removeQuestion(url,q_id)};
    modal.style.display = "block";
}

function removeQuestion(url, q_id) {
    $.ajax({
        type: "GET",
        data: {'question_id': q_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#questionView");
        }
    });
    document.getElementById("modalPopUp").style.display = "none";;
}

function removeAnswer(url, a_id, index) {
     $.ajax({
        type: "GET",
        data: {'answer_id': a_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#question-edit-" + index);
        }
    });
}

function addQuestionContent(q_id){
    
    document.getElementById("question-form-" + q_id).style.display = "block";
};

function addAnswerContent(q_id, a_id){
    document.getElementById("answer-form-" + q_id + "-" + a_id).style.display = "block";
};

function shiftQuestion(url, q_id, direction) {
    
    $.ajax({
        type: "GET",
        data: {'question_id': q_id,
                'direction': direction},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#questionView");
        }
    });
};

function refresh(section)
{
    console.log("Beginning Refresh")
    // $(section).load(document.URL + section);
    $.ajax({
        type: "GET",
        url: document.URL,
        contentType: "text",
        success: function(data) {
            var result = $('<div />').append(data).find(section).html();
            if(typeof $(section)[0] !== 'undefined')
            {
                $(section)[0].innerHTML = result;
            }
            if(document.URL.indexOf("quizzes"))
            {
                $('#account-tables').DataTable();
            }
            MathJax.typeset();
            console.log("Refreshed");
        }
    })
    // console.log("Refreshed");
};

function showEditQuestionContainer(index) {
    document.getElementById("question-display-" + index).style.display = "none";
    document.getElementById("question-edit-" + index).style.display = "block";
}

function resetEditQuestionContainer(index) {
    document.getElementById("question-display-" + index).style.display = "block";
    document.getElementById("question-edit-" + index).style.display = "none";
}

function showEditQuizNameContainer() {
    document.getElementById("quizname").style.display = "none";
    document.getElementById("quiz-name-edit-form").style.display = "inline-block";
}

function resetEditQuizNameContainer() {
    document.getElementById("quizname").style.display = "inline-block";
    document.getElementById("quiz-name-edit-form").style.display = "none";
}

function setQType(url,question_id, qtype) {
    event.preventDefault();
    $.ajax({
        type: "GET",
        data: {'question_id': question_id,
                'qtype': qtype},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#questionView");
        }
    });
    
};

function change_active_question(url,question_id,quiz_id) {
    $(this).focus();
    event.preventDefault();
    $.ajax({
        type: "GET",
        data: {'question_id': question_id,
                'quiz_id': quiz_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#questionView");
        }
    });
};

function setAnswer(url,answer_id,classroom_id, page_num,quiz_id,value){
    event.preventDefault();
    console.log('were in');
    $.ajax({
        type: "GET",
        data: {'answer_id': answer_id, 'classroom_id': classroom_id, 
        'page_num': page_num, 'quiz_id':quiz_id, 'value':value},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#questionView");
        }
    });
}

function showTrueFalse(answer_id){
    event.preventDefault();
    var form_content = document.getElementById(answer_id+'-TF-form');
    var question_content = document.getElementById('question-content-display-' + answer_id);
    var answer_choices = document.getElementById(answer_id + '-answerchoices');
    answer_choices.classList.replace('show', 'noshow');
    form_content.classList.replace('noshow', 'show');
    question_content.classList.replace('show', 'noshow');
    
}

function  cancelTF(answer_id){
    event.preventDefault();
    var form_content = document.getElementById(answer_id+'-TF-form');
    var question_content = document.getElementById('question-content-display-' + answer_id);
    var answer_choices = document.getElementById(answer_id + '-answerchoices');
    answer_choices.classList.replace('noshow', 'show');
    form_content.classList.replace('show', 'noshow');
    question_content.classList.replace('noshow', 'show');
}

function setTF(number, index, span) {
    console.log(span);
    var choice = span.innerHTML;
    console.log(choice);
    // find the form checkbox
    console.log("looking for " + "aform-" + choice.toLowerCase() + "-" + index);
    var checkbox = document.getElementById("aform-" + choice.toLowerCase() + "-" + index);
    console.log("checkbox: ");
    console.log(checkbox);
    // figure out which button it is and color it accordingly
    if(choice == 'True') {
        var other = document.getElementById("aform-false-" + (index+1));
        var otherBtn = document.getElementById("btn-false-" + (index+1));
         $(span).toggleClass('btn-success btn-outline-success');
         $(otherBtn).toggleClass('btn-danger btn-outline-danger');
    } else {
        var other = document.getElementById("aform-true-" + (index-1));
        var otherBtn = document.getElementById("btn-true-" + (index-1));
        $(span).toggleClass('btn-danger btn-outline-danger');
        $(otherBtn).toggleClass('btn-success btn-outline-success');
    }
    console.log("other: ");
    console.log(other);
    // toggle the checkbox
    if(checkbox.checked) {
            console.log("was checked");
            checkbox.removeAttribute("checked");
            checkbox.value = 'n';
            other.setAttribute("checked", "checked");
            other.value = 'y';
        } else {
            console.log("was unchecked");
            checkbox.setAttribute("checked", "checked");
            checkbox.value = 'y';
            other.removeAttribute("checked");
            other.value = 'n';
        }
        console.log("checkbox: ");
    console.log(checkbox);
    console.log("other: ");
    console.log(other);
    refresh("#question-edit-" + number);
}


/**
 * Description:
        Handles aligning the checkbox and the buttons for backend procesing
        Handles the display after form submission
 * Param:
        span:
            either span the given is the true span or the false span tag from the dom
 * Return: 
        n/a
 */
function checked(span){
    if(span.title === 'True'){
        var id = span.id.slice(9);
    }
    else{
        var id = span.id.slice(10);
    }
    
    var true_checkbox_id = 'answer_form-true-' + id;
    var false_checkbox_id = 'answer_form-false-' + id;
    
    //Display Processing variables
    var true_display = document.getElementById(id+'-true-display');
    var false_display = document.getElementById(id+'-false-display');
    
    /*Processing the data for the backend section */
    if(span.title === 'True'){
        console.log(span.id.slice(0,9) + id);
        var false_button = document.getElementById('btn-false-' + id);
        console.log('false button is ' + false_button);
        if (false_button.classList.contains('active')){
            false_button.classList.remove('active');
        }
        span.classList.add('active');

        var true_checkbox = document.getElementById(true_checkbox_id);
        true_checkbox.checked = true;

        var false_checkbox = document.getElementById(false_checkbox_id);
        false_checkbox.checked = false;


    }
    else{
        
        var true_button = document.getElementById('btn-true-' + id);
        if(true_button.classList.contains('active')){
            true_button.classList.remove('active');
        }
        span.classList.add('active');
        
        var false_checkbox = document.getElementById(false_checkbox_id);
        false_checkbox.checked = true;

        var true_checkbox = document.getElementById(true_checkbox_id);
        true_checkbox.checked = false;
        
        
    
         
    }

    
    

    
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
    var classroom = document.getElementById('classroom-' + classroom_id);
    var form = document.getElementById('classroom-form-'+ classroom_id);
    classroom.style.display='none';
    form.style.display = 'block';
}

function cancelEditClassroom(classroom_id){
    var classroom = document.getElementById('classroom-' + classroom_id);
    var form = document.getElementById('classroom-form-'+ classroom_id);
    classroom.style.display='inline-block';
    form.style.display = 'none';
}

function showShortAnswer(question_id){
    event.preventDefault();
    var form_content = document.getElementById(question_id+'-short-answer-form');
    var question_content = document.getElementById('question-content-display-' + question_id);
    var answer_choices = document.getElementById(question_id + '-answerchoices');
    answer_choices.classList.replace('show', 'noshow');
    form_content.classList.replace('noshow', 'show');
    question_content.classList.replace('show', 'noshow');
}

function checkCorrect(index) {
    var icon = document.getElementById("checkbox-" + index);
    console.log(icon);
    $(icon).toggleClass("fas far");
    // change appearance of checkbox icon
    var checkbox = document.getElementById("answer_form-" + index + "-correct");
    console.log(checkbox);
    // check the form's actual checkbox
    if(checkbox.checked) {
        console.log("checkbox was checked");
        checkbox.checked = false;
    } else {
        console.log("checkbox was unchecked");
        checkbox.checked = true;
    }
}

/*  Removal of a Quiz*/
function removeQuizPopup(url, q_id) {
    modal = document.getElementById("modalPopUp");
    modalText = document.getElementById("modalText")
    modalButton = document.getElementById("modalButton");
    modalText.innerHTML = "Are you sure that you want to delete this quiz??";
    modalButton.onclick = function() {removeQuiz(url,q_id)};
    modal.style.display = "block";
}

function removeQuiz(url, q_id) {
    $.ajax({
        type: "GET",
        data: {'quiz_id': q_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#quizListing");
        }
    });
    document.getElementById("modalPopUp").style.display = "none";
}

// create Quiz
function createQuizPopup() {
    document.getElementById("modalPopUpForm").style.display = "none";
    modal = document.getElementById("modalPopUpForm");
    modalForm = document.getElementById("modalQuiz");
    modalText = document.getElementById("modalTextForm");
    modalText.innerHTML = "Create Quiz";
    modal.style.display = "block";
    modalForm.style.display = "block";
    refresh("#quizListing");
}