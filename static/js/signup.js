function checkUsername() {
  const id = document.querySelector('input[name="id"]').value;
  const resultDiv = document.getElementById('usernameCheckResult');

  if (id.length < 6 || id.length > 20) {
    resultDiv.textContent = '아이디는 6자 이상 20자 이하로 입력해 주세요.';
    resultDiv.style.display = 'block';
  } else {
    resultDiv.textContent = '';
    resultDiv.style.display = 'none';
  }
}

function checkEmail() {
  const email = document.querySelector('input[name="email"]').value;
  const emailResultDiv = document.getElementById('emailCheckResult');
  const emailPattern = /^[a-zA-Z0-9._%+-]+@(naver|gmail|daum)\.com$/;

  if (!emailPattern.test(email)) {
    emailResultDiv.textContent = '이메일 양식이 틀렸습니다.';
    emailResultDiv.style.display = 'block';
  } else {
    emailResultDiv.textContent = '';
    emailResultDiv.style.display = 'none';
  }
}

document.querySelector('input[name="email"]').addEventListener('focusout', checkEmail);

function checkPassword() {
  const pwd1 = document.querySelector('input[name="pw"]').value;
  const pwd2 = document.querySelector('input[name="pw_ch"]').value;
  const pwResultDiv = document.getElementById('pwCheckResult');

  if (pwd1.length < 8 || pwd1.length > 20) {
    pwResultDiv.textContent = '비밀번호는 8자 이상 20자 이하이어야 합니다.';
    pwResultDiv.style.color = 'red';
    pwResultDiv.style.display = 'block';
    return false;
  }

  if (pwd1 !== pwd2) {
    pwResultDiv.textContent = '비밀번호가 일치하지 않습니다.';
    pwResultDiv.style.color = 'red';
    pwResultDiv.style.display = 'block';
    return false;
  } else {
    pwResultDiv.textContent = '비밀번호가 일치합니다.';
    pwResultDiv.style.color = 'green';
    pwResultDiv.style.display = 'block';
    return true;
  }
}

document.querySelectorAll('input[name="pw"], input[name="pw_ch"]').forEach(input => {
  input.addEventListener('input', checkPassword);
});

function checkStuff(event) {
  const name = document.querySelector('input[name="name"]').value;
  const phone = document.querySelector('input[name="tel"]').value;
  const email = document.querySelector('input[name="email"]').value;
  const address = document.querySelector('input[name="address"]').value;
  const position = document.getElementById("position").value;
  const errorMsg = document.getElementById('msg');

  if (name === "" || phone === "" || email === "" || address === "" || position === "직책") {
    errorMsg.textContent = '빈칸을 입력해 주세요.';
    errorMsg.style.display = 'block';
    return false;
  }

  errorMsg.style.display = 'none';

  // 성공 메시지 표시 및 2초 후 로그인 페이지로 이동
  const successMessage = document.getElementById('successMessage');
  successMessage.style.display = 'block';
  setTimeout(() => {
    window.location.href = location.href='http://127.0.0.1:5000/'; // 로그인 페이지로 이동
  }, 2000);

  return false; // 폼 제출 중단
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('form[name="form1"]').onsubmit = checkStuff;
});
