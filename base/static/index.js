function changeStatus(){
    var element = document.getElementById("followButton");
    if (element.value == "Follow") element.value = "Unfollow";
    else element.value = "Follow";
}