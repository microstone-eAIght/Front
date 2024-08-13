function togglePass() {
    // Toggle the 'active' class on the eye icon
    eye.classList.toggle('active');

    // Toggle the type of the password field between 'password' and 'text'
    pwd.type = (pwd.type === 'password') ? 'text' : 'password';
}

// Form Validation
function checkStuff() {
    var email = document.form1.아이디; // Ensure HTML input field name is '아이디'
    var password = document.form1.비밀번호; // Ensure HTML input field name is '비밀번호'
    var msg = document.getElementById('msg');

    if (email.value === "") {
        msg.style.display = 'block';
        msg.innerHTML = "아이디를 입력해 주세요";
        email.focus();
        return false;
    } else {
        msg.innerHTML = "";
    }

    if (password.value === "") {
        msg.innerHTML = "비밀번호를 입력해 주세요";
        password.focus();
        return false;
    } else {
        msg.innerHTML = "";
    }

}
