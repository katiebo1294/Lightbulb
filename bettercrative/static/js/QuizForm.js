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
            refresh("#body");
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
            refresh("#body");
        }
    });
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
            refresh("#body");
        }
    });
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
            refresh("#body");
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
            refresh("#body");
        }
    });
};

function refresh(section)
{
    console.log("Beginning Refresh")
    $(section).load(section);
    console.log("Refreshed");
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
            refresh("#body");
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
            refresh("#body");
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
            refresh("#body");
        }
    });
}

function showTrueFalse(answer_id,choice,answers){
    console.log(answer_id);
    var button = document.getElementById(answer_id+'-btn');
    console.log(button);
    button.classList.add('active');
    console.log(choice);
    console.log(button);


    if(choice == 'true'){
        button = document.getElementById(answer_id+'-btn');
        button.classList.remove('active');
    }
    else{
        button = document.getElementById(answer_id+'-btn');
        button.classList.remove('active');
    }
    
    document.getElementById("check_button").style.display = "block";
    event.preventDefault();
    
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
function checked(answer_id){
    //Get the button and the checkbox
    var button = document.getElementById(answer_id+'-correct');
    var checkbox = document.getElementById(answer_id + '-checkbox');
    

    //Checking rules for checkbox
    var contains = button.classList.length
    if(button.classList.item(contains-1) === 'active'){
        button.classList.remove('active');
        checkbox.checked = false;
    }
    else{
        checkbox.checked = true;
        button.classList.add('active');
    }
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