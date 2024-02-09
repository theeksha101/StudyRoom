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
