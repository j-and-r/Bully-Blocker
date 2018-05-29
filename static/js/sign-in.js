window.onload = function() {

  submit = function () {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var confirm_password = document.getElementById('password-confirm');
    if (confirm_password == null) {
      confirm_password = password;
    } else {
      confirm_password = confirm_password.value;
    }
    var error = document.getElementById('error');
    var email_regex = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;

    console.log(password);
    console.log(confirm_password);

    if (password != confirm_password) {
      error.innerHTML = "Passwords do not match";
    } else if (password == "") {
      error.innerHTML = "Must provide password";
    } else if (email == "") {
      error.innerHTML = "Must provide email";
    } else if (email.match(email_regex) == null) {
      error.innerHTML = "Email is not valid";
    } else {
      document.getElementById('form').submit();
    }
  }

  document.addEventListener('keypress', function(e) {
    var key = e.key;
    if(key == "Enter") {
      var inputs = document.getElementsByTagName('input');
      var form = document.getElementById('form');
      var activeElement = document.activeElement;
      if(activeElement.hasAttribute('id')) {
        var active_id = activeElement.getAttribute('id');
        var n = 0;

        for(var i = 0; i < inputs.length; i++) {
          if(inputs[i].getAttribute('id') == active_id) {
            n = i;
            break;
          }
        }
        console.log(n);
        console.log(inputs);
        if(n+1 == inputs.length) {
          submit();
        } else {
          inputs[n+1].focus();
        }
      }
    }
  });
}
