//
//
//spans = document.querySelectorAll('span');
//for (var j = 0; j < spans.length; j++) {
//    spans[j].classList.add('d-block');
//}
//
//
//labels = document.querySelectorAll('label');
//
//for (var i = 0; i < labels.length; i++) {
//    labels[i].classList.add('form-label');
//}
//
//inputs = document.querySelectorAll('input');
//for (var i = 0; i < inputs.length; i++) {
//    inputs[i].classList.add('form-control');
//}
//select= document.querySelector('select')
//
//select.classList.add('form-control')
//
//divs = document.getElementsByClassName("form_element")
//for (var d =0; d < divs.length; d++){
//    divs[d].classList.add('mb-3')
//}
//
//checkboxex=document.querySelectorAll('input[type="checkbox"]')
//for (var d =0; d < checkboxex.length; d++){
//    checkboxex[d].classList.remove('form-control')
//}
////var checkbox = document.querySelector('input[name="image-clear"]');
////        checkbox.addEventListener('click', function() {
////            // When the "image-clear" checkbox is clicked, clear the value of the image field
////            var imageField = document.querySelector('input[name="image"]');
////            imageField.value = '';
////            }
//
//errors = document.getElementsByClassName('errorlist')
//for (var m=0 ; m < errors.length; m ++){
//    errors[m].style.color = 'red';
//}
////errors = document.getElementsByClassName('errorlist');
////for (var m = 0; m < errors.length; m++) {
////    errors[m].style.color = 'red';
////    errors[m].style.fontWeight = 'bold';
////}
// Add Bootstrap classes to form elements
document.addEventListener("DOMContentLoaded", function() {
  // Add form-control class to input fields
//  var input=document.querySelectorAll("input");
//  input.forEach
  var inputFields = document.querySelectorAll("input[type='text'], input[type='email'], input[type='password']");
  inputFields.forEach(function(input) {
    input.classList.add("form-control");
    input.classList.add("col-4"); // Set width to 8 columns out of 12
  });

  // Add form-group class to div containers
  var divContainers = document.querySelectorAll("div");
  divContainers.forEach(function(div) {
    div.classList.add("form-group");
  });

  // Add label class to labels
  var labels = document.querySelectorAll("label");
  labels.forEach(function(label) {
    label.classList.add("form-label");
  });

  // Add helptext class to divs with class "helptext"
  var helptextDivs = document.querySelectorAll(".helptext");
  helptextDivs.forEach(function(div) {
    div.classList.add("form-text");
    div.classList.add("text-muted");
  });

  // Add btn class to submit button
  var submitButton = document.querySelector("input[type='submit']");
  submitButton.classList.add("btn");
  submitButton.classList.add("btn-primary");
  submitButton.classList.add("mx-auto");

});
