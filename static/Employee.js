// Employee.js

document.addEventListener('DOMContentLoaded', () => {
    loadEmployees();
    document.getElementById('addEmployeeButton').addEventListener('click', showAddEmployeeForm);

    // 모달 창 닫기 이벤트
    document.querySelector('.close').addEventListener('click', () => {
        document.getElementById('employeeModal').style.display = 'none';
    });

    // 폼 제출 이벤트
    document.getElementById('employeeForm').addEventListener('submit', handleFormSubmit);
});

function loadEmployees() {
    fetch('http://localhost:5000/Employee')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const tableBody = document.querySelector('#employeeTable tbody');
            tableBody.innerHTML = doc.querySelector('#employeeTable tbody').innerHTML;
        })
        .catch(error => {
            console.error('Error loading employees:', error);
        });
}

function showAddEmployeeForm() {
    document.getElementById('employeeModal').style.display = 'block';
    document.getElementById('modalTitle').textContent = '직원 추가하기';
    clearForm();
}

function showEditEmployeeForm(id) {
    // API 없는 경우, 주석처리
    /*
    fetch(`/api/employees/${id}`)
        .then(response => response.json())
        .then(data => {
            const employee = data.employee;
            document.getElementById('employeeModal').style.display = 'block';
            document.getElementById('modalTitle').textContent = '직원 수정하기';
            document.getElementById('name').value = employee.name;
            document.getElementById('region').value = employee.region;
            document.getElementById('department').value = employee.department;
            document.getElementById('position').value = employee.position;
            document.getElementById('phone').value = employee.phone;
            document.getElementById('email').value = employee.email;
            document.getElementById('employeeForm').dataset.id = employee.id;
        });
    */
}

function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const id = form.dataset.id;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/employees/${id}` : '/api/employees';
    const data = {
        id: id || generateEmployeeId(),
        name: form.name.value,
        region: form.region.value,
        department: form.department.value,
        position: form.position.value,
        phone: form.phone.value,
        email: form.email.value
    };

    // API 없는 경우, 주석처리
    /*
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(() => {
        form.reset();
        document.getElementById('employeeModal').style.display = 'none';
        loadEmployees();
    });
    */
}

function deleteEmployee(id) {
    // API 없는 경우, 주석처리
    /*
    if (confirm('정말로 삭제하시겠습니까?')) {
        fetch(`/api/employees/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(() => {
            loadEmployees();
        });
    }
    */
}

function clearForm() {
    document.getElementById('employeeForm').reset();
    delete document.getElementById('employeeForm').dataset.id;
}
