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

let employeeCounter = 0;

function loadEmployees() {
    fetch('/api/employees')
        .then(response => response.json())
        .then(data => {
            const employees = data.employees;
            const tableBody = document.querySelector('#employeeTable tbody');
            tableBody.innerHTML = '';
            employees.forEach(employee => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${employee.id}</td>
                    <td>${employee.name}</td>
                    <td>${employee.region}</td>
                    <td>${employee.department}</td>
                    <td>${employee.position}</td>
                    <td>${employee.phone}</td>
                    <td>${employee.email}</td>
                    <td><button onclick="showEditEmployeeForm(${employee.id})" class="btn small-btn">수정</button></td>
                    <td><button onclick="deleteEmployee(${employee.id})" class="btn small-btn">삭제</button></td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function showAddEmployeeForm() {
    document.getElementById('employeeModal').style.display = 'block';
    document.getElementById('modalTitle').textContent = '직원 추가하기';
    clearForm();
}

function showEditEmployeeForm(id) {
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
}

function generateEmployeeId() {
    employeeCounter += 1;
    return String(employeeCounter).padStart(3, '0');
}

function deleteEmployee(id) {
    if (confirm('정말로 삭제하시겠습니까?')) {
        fetch(`/api/employees/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(() => {
            loadEmployees();
        });
    }
}

function clearForm() {
    document.getElementById('employeeForm').reset();
    delete document.getElementById('employeeForm').dataset.id;
}
