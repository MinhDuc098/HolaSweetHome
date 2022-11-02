function showPassword() {
    var array = document.getElementsByClassName("password");
    for (var i = 0; i < array.length; i++) {
        if (array[i].type === "password") {
            array[i].type = "text";
        } else {
            array[i].type = "password";
        }
    }
}