    //adjusts indices of form fields when removing items
    function adjustIndices(removedIndex) {
    var $forms = $('.subform');

    $forms.each(function(i) {
        var $form = $(this);
        var index = parseInt($form.data('index'));
        var newIndex = index - 1;

        if (index < removedIndex) {
            // Skip
            return true;
        }

        // Change ID in form itself
        $form.attr('id', $form.attr('id').replace(index, newIndex));
        $form.data('index', newIndex);

        // Change IDs in form inputs
        $form.find('input').each(function(j) {
            var $item = $(this);
            $item.attr('id', $item.attr('id').replace(index, newIndex));
            $item.attr('name', $item.attr('name').replace(index, newIndex));
        });
    });
}

//remove a subform
function removeForm() {
    var $removedForm = $(this).closest('.subform');
    var removedIndex = parseInt($removedForm.data('index'));

    $removedForm.remove();

    // Update indices
    adjustIndices(removedIndex);
}


function addQuestion(url, q_id) {
    
    $.ajax({
        type: "GET",
        data: {'quiz_id': q_id},
        url: url,
        error: function(statusText) {
            alert(statusText);
            console.log(statusText);
        },
        success: function() {
            refresh("#body");
        }
    });
}
function addAnswer() {

}
function removeQuestion(url, q_id) {
    $.ajax({
        type: "GET",
        data: {'question_id': q_id},
        url: url,
        error: function(statusText) {
            alert(statusText);
            console.log(statusText);
        },
        success: function() {
            refresh("#body");
            //$("#question-" + q_id).hide();
        }
    });
}
function removeAnswer() {

}
//add a subform
function addForm() {
    var $templateForm = $('#question-_-form');

    if (!$templateForm) {
        console.log('[ERROR] Cannot find template');
        return;
    }

    // Get Last index
    var $lastForm = $('.subform').last();

    var newIndex = 0;

    if ($lastForm.length > 0) {
        newIndex = parseInt($lastForm.data('index')) + 1;
    }

    // Maximum of 20 subforms
    if (newIndex > 20) {
        console.log('[WARNING] Reached maximum number of elements');
        return;
    }

    // Add elements
    var $newForm = $templateForm.clone();

    $newForm.attr('id', $newForm.attr('id').replace('_', newIndex));
    $newForm.data('index', newIndex);

    $newForm.find('input').each(function(idx) {
        var $item = $(this);

        $item.attr('id', $item.attr('id').replace('_', newIndex));
        $item.attr('name', $item.attr('name').replace('_', newIndex));
    });

    // Append
    $('#subforms-container').append($newForm);
    $newForm.addClass('subform');
    $newForm.removeClass('is-hidden');

    $newForm.find('.remove').click(removeForm);
}

function addQuestionContent(q_id){
    
    document.getElementById("question-form-" + q_id).style.display = "block";
};

function shiftQuestion(url, q_id, direction) {
    
    $.ajax({
        type: "GET",
        data: {'question_id': q_id,
                'direction': direction},
        url: url,
        error: function(statusText) {
            alert(statusText);
            console.log(statusText);
        },
        success: function() {
            refresh("#body");
        }
    });
}

$(document).ready(function() {
    // $('#add').click(addForm);
    // $('.remove').click(removeForm);
});

function refresh(section)
{
    console.log("Beggining Refresh")
    $(section).load(section);
    console.log("Refreshed");
};



