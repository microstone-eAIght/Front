// Function to toggle the visibility of the error message
function toggleError(inputElement, message) {
    const errorSpan = inputElement.nextElementSibling; // Get the next sibling (the error message span)
    if (inputElement.value.trim() === "") { // Check if input is empty
        errorSpan.textContent = message; // Set error message
        errorSpan.style.display = 'block'; // Show error message
    } else {
        errorSpan.textContent = ""; // Clear error message
        errorSpan.style.display = 'none'; // Hide error message
    }
  }
  
  // Function to handle form validation
  function checkStuff() {
    const id = document.querySelector('input[name="아이디"]');
    const password = document.querySelector('input[name="비밀번호"]');
    
    let isValid = true;
    
    // Validate id
    if (id.value.trim() === "") {
        toggleError(id, "아이디를 입력하세요.");
        isValid = false;
    } else {
        toggleError(id, "");
    }
    
    // Validate password
    if (password.value.trim() === "") {
        toggleError(password, "비밀번호를 입력하세요.");
        isValid = false;
    } else {
        toggleError(password, "");
    }
  
    // Return false if any field is invalid
    return isValid;
  }
  
  // Add event listeners to hide error messages when inputs are focused
  document.querySelector('input[name="아이디"]').addEventListener('focus', function() {
    this.nextElementSibling.style.display = 'none';
  });
  
  document.querySelector('input[name="비밀번호"]').addEventListener('focus', function() {
    this.nextElementSibling.style.display = 'none';
  });
  