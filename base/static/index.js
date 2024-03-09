function changeStatus(button){
    var topicName = $(button).data('topic');
    console.log(topicName)
    $.ajax({
        method: 'POST',
        url: '/toggle_follow/',
        data: {'topic_name': topicName},
        success: function(response){
            alert(response.message);

            if (button.value === 'Follow'){
                button.value = 'Following';
            }
            else{
                button.value = 'Follow';
            }
        },
        error: function(error){
            console.error('Error', error);
        }
    });
}

function joinRoom(button){
    var room_id = $(button).data('id');
    console.log(room_id)
    $.ajax({
        method: 'POST',
        url: '/join_room/',
        data: {'room_id': room_id,
                'button_value': button.value},
        success: function(response){

            if (button.value === 'Join'){
                button.value = 'Joined';
            }
            else{
                button.value = 'Join';
            }
        },
        error: function(error){
            console.error('Error', error);
        }
    });
}
