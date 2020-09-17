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
            window.location.reload();
        }
    });
}

function addAnswer(url, q_id, index) {
    event.preventDefault();
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
            window.location.reload();
        }
    });
    document.getElementById("modalPopUp").style.display = "none";;
}

function removeAnswer(url, a_id, index) {
    event.preventDefault();
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

function showEditQuestionContainer(index) {
    document.getElementById("question-display-" + index).style.display = "none";
    document.getElementById("question-edit-" + index).style.display = "block";
}

function resetEditQuestionContainer(index) {
    document.getElementById("question-display-" + index).style.display = "block";
    document.getElementById("question-edit-" + index).style.display = "none";
}

function showEditQuizNameContainer(quiz_id) {
    document.getElementById("quiz-" + quiz_id).style.display = "none";
    document.getElementById("quiz-form-" + quiz_id).style.display = "inline-block";
}

function resetEditQuizNameContainer(quiz_id) {
    document.getElementById("quiz-" + quiz_id).style.display = "inline-block";
    document.getElementById("quiz-form-" + quiz_id).style.display = "none";
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
            window.location.reload();
        }
    });

};

function change_active_question(url,question_id,quiz_id) {
    console.log("switching to question " + question_id);
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
            refresh("#quiz-container");
        }
    });
};

function setAnswer(url,answer_id,classroom_id, page_num,quiz_id,value,student_id){



    $.ajax({
        type: "GET",
        data: {'answer_id': answer_id, 'classroom_id': classroom_id,
        'page_num': page_num, 'quiz_id':quiz_id, 'value':value,'student_id':student_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            refresh("#response-"+quiz_id);

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

function setMC(i){
    console.log(i.classList);
    console.log(i.style.color);
    if(i.style.color === 'rgb(108, 117, 125)'){
        i.style.color = 'green';
    }
    else{
        i.style.color = '#6c757d';
    }


    var id = i.id.slice(9);
    var checkbox = document.getElementById('answer_form-' + id + '-correct');
    if(checkbox.checked){
        checkbox.checked = false;
    }
    else{
        checkbox.checked = true;
    }

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
}

function responseIDE(url,answer_id,classroom_id, page_num,quiz_id,student_id) {
    var editor = ace.edit("editor");
    var code = editor.getValue();
    console.log(code);
    $.ajax({
        type: "GET",
        data: {'answer_id': answer_id, 'classroom_id': classroom_id,
        'page_num': page_num, 'quiz_id':quiz_id, 'value': code,'student_id': student_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
        }
    });
}

function responseMC(answer_id){
    var btn =document.getElementById('question-'+answer_id);
    if(btn.classList.contains('active')){
        btn.classList.remove('active');
    }
    else{
        btn.classList.add('active')
    }
}

function responseTF(question_id, status){
   
    var t = document.getElementById('question-'+question_id+'-true')
    var f = document.getElementById('question-'+question_id+'-false');
    console.log(t);
    if(status === 1){
        f.classList.remove('active');
        t.classList.add('active');
    }
    else{
        t.classList.remove('active');
        f.classList.add('active');
    }
}

function setTextArea(url,answer_id,classroom_id, page_num,quiz_id,student_id){

    var textarea = document.getElementById('textareabox-'+student_id);
    $.ajax({
        type: "GET",
        data: {'answer_id': answer_id, 'classroom_id': classroom_id, 
        'page_num': page_num, 'quiz_id':quiz_id, 'value':textarea.value,'student_id':student_id},
        url: url,
        error: function(response) {
            alert(response.statusText);
            console.log(response.statusText);
        },
        success: function() {
            
        }
    });
}

// makes question buttons sortable by dragging them with the mouse
$("#questions-menu").sortable({
    axis: "x",
    start: function(event, ui) {
        console.log("begin sort");
        ui.item.startPos = ui.item.index();
    }, stop: function(event, ui) {
        console.log("end sort");
        ui.item.endPos = ui.item.index();
        console.log("moved from " + ui.item.startPos + " to " + ui.item.endPos);
        var quiz_id = document.getElementsByClassName('editTitle')[0].id.slice(5);
        console.log(quiz_id);
        $.ajax({
           type: "GET",
           data: {'startPos': ui.item.startPos, 'endPos': ui.item.endPos, 'quiz_id': quiz_id},
           url: '/quiz/shift_question',
           error: function(response) {
            console.log(response.statusText);
           },
           success: function() {
               window.location.reload();
           }
        });
    }
});

// makes question buttons sortable by using the arrow keys
$("div[id^='qbtn-']").keyup(function(e) {
    if(e.keyCode == 37 || e.keyCode == 39) {
        var quiz_id = document.getElementsByClassName('editTitle')[0].id.slice(5);
        var length = $('#questions-menu div').length;
        var startPos = this.id.slice(5) - 1;
        var endPos = startPos;
        var method = "keypress";
        if(e.keyCode == 37) {
            if(startPos > 0) {
                var direction = 'left';
                endPos = startPos - 1;
                console.log(direction + " pressed on button " + startPos);
            }
        } else if(e.keyCode == 39) {
            if(startPos < length) {
                var direction = 'right';
                endPos = startPos + 1;
                console.log(direction + " pressed on button " + startPos);
            }
        }
        $.ajax({
           type: "GET",
           data: {'startPos': startPos, 'endPos': endPos, 'quiz_id': quiz_id},
           url: '/quiz/shift_question',
           error: function(response) {
                console.log(response.statusText);
           },
           success: function() {
                window.location.reload();
           }
        });
    // enter key
    } else if(e.keyCode == 13) {
        console.log(this);
        this.click();
    }
});

