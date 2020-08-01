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

function addAnswer(url, q_id) {
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
}
// remove Question
function removeQuestionPopup(url, q_id) {
    modal = document.getElementById("modalPopUp");
    modalText = document.getElementById("modalTextDeleteQuestion")
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

function removeAnswer(url, a_id) {
     $.ajax({
        type: "GET",
        data: {'answer_id': a_id},
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
            $(section)[0].innerHTML = result;
            console.log("Refreshed");
        }
    })
    // console.log("Refreshed");
};

function showEditQuestionContainer(index) {
    
    document.getElementById("question-content-display-" + index).style.display = "none";
    document.getElementById("question-content-edit-form-" + index).style.display = "block";
    document.getElementById("displayAnswer-" + index).style.display = "none";
    document.getElementById("displayAnswerEdit-" + index).style.display = "block";
};

function showEditQuizNameContainer() {
    document.getElementById("quizname").style.display = "none";
    document.getElementById("quiz-name-edit-form").style.display = "inline-block";
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


function setTrueFalse(choice){
    var t = document.getElementById('true-btn');
    var f = document.getElementById('false-btn');

    console.log(t);
    console.log(f);

    if (t.classList[t.classList.length -1] === 'active'){
        setAnswer();
    }
    else{
        setAnswer();
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

$('.correctness-container').click(function() {
    var icon = $(this).find('i');
    var id = icon.attr('id');
    id = id.slice(0, id.length - 8);
    console.log(id);
    icon.toggleClass('far fa-check-circle fas fa-check-circle');
    var checkbox = $(this).find('#' + id + "correct");
    console.log(checkbox);
    if(checkbox.prop('checked')) {
        console.log('was checked');
        checkbox.prop('checked', false);
    } else {
        console.log('was not checked');
        checkbox.prop('checked', true);
    }
});

