var pwd = document.getElementById('pwd');

eye.addEventListener('click', togglePass);

function togglePass() {
  eye.classList.toggle('active');

  pwd.type == 'password' ? (pwd.type = 'text') : (pwd.type = 'password');
}

// Form Validation

function checkStuff() {
  var email = document.form1.email;
  var password = document.form1.password;
  var msg = document.getElementById('msg');

  if (email.value == NULL) {
    msg.style.display = 'block';
    msg.innerHTML = 'Please enter your email';
    email.focus();
    return false;
  } else {
    msg.innerHTML = NULL;
  }

  if (password.value == NULL) {
    msg.innerHTML = 'Please enter your password';
    password.focus();
    return false;
  } else {
    msg.innerHTML = NULL;
  }
  var re =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (!re.test(email.value)) {
    msg.innerHTML = 'Please enter a valid email';
    email.focus();
    return false;
  } else {
    msg.innerHTML = NULL;
  }
}
