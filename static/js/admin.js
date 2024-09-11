function searchEmployee() {
    // 직원 검색 폼을 보여주도록 변경
    showsearchEmployeeForm();
}

// 직원 데이터를 예제로 추가
const employees = [
    {id: 1, name: '홍길동', region: '서울', department: '부서1', position: '1', phone: '010-1234-5678', email: 'hong@example.com'},
    {id: 2, name: '김철수', region: '부산', department: '부서2', position: '2', phone: '010-2345-6789', email: 'kim@example.com'},

];

document.addEventListener('DOMContentLoaded', function() {
    const tbody = document.querySelector('#employeeTable tbody');
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
            <td><button class="kakao-button" onclick="sendKakaoMessage('${employee.phone}')">전송</button></td> <!-- 카카오톡 전송 버튼 추가 -->
        `;
        tbody.appendChild(row);
    });

    document.querySelector('.close').addEventListener('click', function() {
        document.getElementById('employeeModal').style.display = 'none';
    });
});

function showsearchEmployeeForm() {
    document.getElementById('employeeModal').style.display = 'block';
    document.getElementById('modalTitle').textContent = '직원 검색';
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

function clearForm() {
    document.getElementById('name').value = '';
    document.getElementById('region').value = '';
    document.getElementById('department').value = '';
    document.getElementById('position').value = '';
    document.getElementById('phone').value = '';
    document.getElementById('email').value = '';
    document.getElementById('employeeForm').dataset.id = '';
}

function sendKakaoMessage() {
    alert(`카카오톡 메시지 전송`);
    // 실제로는 카카오톡 API를 사용하여 메시지를 전송
}
