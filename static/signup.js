function checkStuff() {
    const id = document.querySelector('input[name="id"]').value;
    const password = document.querySelector('input[name="pw"]').value;
    const confirmPassword = document.querySelector('input[name="pw_ch"]').value;
    const name = document.querySelector('input[name="name"]').value;
    const phone1 = document.getElementById("phone1").value;
    const phone2 = document.getElementById("phone2").value;
    const phone3 = document.getElementById("phone3").value;
    const email1 = document.getElementById("email1").value;
    const emailSelect = document.getElementById("email").value;
    const position = document.getElementById("position").value;
    const errorMsg = document.getElementById('msg'); 
    const specialCharPattern = /[!@#$%^&*(),.?":{}|<>]/;

    if (id.length < 6 || id.length > 20) {
        errorMsg.textContent = '아이디는 6자 이상 20자 이하로 입력해 주세요.';
        errorMsg.style.display = 'block';
        return false;
    }

    if (password.length < 8 || password.length > 20) {
        errorMsg.textContent = '비밀번호는 8자 이상 20자 이하로 입력해 주세요.';
        errorMsg.style.display = 'block';
        return false;
    }

    if (!specialCharPattern.test(password)) {
        errorMsg.textContent = '비밀번호에 특수문자가 필요합니다.';
        errorMsg.style.display = 'block';
        return false;
    }

    if (password !== confirmPassword) {
        errorMsg.textContent = '비밀번호가 일치하지 않습니다.';
        errorMsg.style.display = 'block';
        return false;
    }

    if (name === "" || phone1 === "" || phone2 === "" || phone3 === "" || email1 === "" || emailSelect === "이메일" || position === "직책") {
        errorMsg.textContent = '빈칸을 입력해 주세요.';
        errorMsg.style.display = 'block';
        return false;
    }

    errorMsg.style.display = 'none';
    showModal();
    return false;
}

function showModal() {
    const modal = document.getElementById("myModal");
    const span = document.getElementsByClassName("close")[0];

    modal.style.display = "block";

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form[name="form1"]').onsubmit = checkStuff;
});
