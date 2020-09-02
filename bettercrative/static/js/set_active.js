function set_active(classroom_id, quiz_id, status){

    $.ajax({
        type:'GET',
        data:{'classroom_id': classroom_id, 'quiz_id': quiz_id, 'status': status},
        url: '/classroom/'+classroom_id+'/'+quiz_id+'/set_active',
        error: function(response){
            console.log(response.statusText);
        },
        success: function(){

            refresh('.account-tables');

        }
    })
}

function remove_active(classroom_id){
    $.ajax({
        type:'GET',
        data:{'classroom_id': classroom_id},
        url: '/classroom/'+classroom_id+'/remove_active',
        error: function(response){
            console.log(response.statusText);
        },
        success: function(){

            refresh('.account-tables');

        }
    })
}