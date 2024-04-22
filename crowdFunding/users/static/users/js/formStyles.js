document.addEventListener("DOMContentLoaded", function() {

errors = document.getElementsByClassName('errorlist');
    for (var m=0 ; m < errors.length; m ++){
    errors[m].style.color = 'red';
}
inputs = document.querySelectorAll("input[type='text'], input[type='email'], input[type='password'],input[type='file']");
for (var i = 0; i < inputs.length; i++) {
    inputs[i].classList.add('form-control');
}
var label = document.getElementById('photoLabel');
var fileInput = document.getElementById('id_photo');

// Add Bootstrap classes to label
label.classList.add('form-control-label');

// Add Bootstrap classes to file input
fileInput.classList.add('form-control-file');
checkboxes=document.querySelectorAll('input[type="checkbox"]')
for (var d =0; d < checkboxes.length; d++){
    checkboxes[d].classList.remove('form-control')
}
});
