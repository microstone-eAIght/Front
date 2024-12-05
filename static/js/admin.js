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

const logoutButton = document.getElementById('logoutButton');

// 사용자 이름과 알림 수를 업데이트하는 함수
function updateUserInfo() {
  const userNameElement = document.getElementById('userName');
  const notificationCountElement =
    document.getElementById('notificationCount');

  userNameElement.textContent = user.name;
  notificationCountElement.textContent = user.notifications;
}

document.addEventListener('DOMContentLoaded', function() {
  const tbody = document.querySelector('#employeeTable tbody');
  const searchButton = document.getElementById('searchButton');
  
  // 초기 직원 리스트 표시
  displayEmployees(employees, tbody);

  // 검색 버튼 클릭 이벤트
  searchButton.addEventListener('click', function() {
      const nameInput = document.getElementById('name').value.trim();
      const filteredEmployees = employees.filter(employee => 
          employee.name.includes(nameInput)
      );
      displayEmployees(filteredEmployees, tbody);
  });

  document.querySelector('.close').addEventListener('click', function() {
      document.getElementById('employeeModal').style.display = 'none';
  });
});

// 직원 리스트 표시 함수
function displayEmployees(employees, tbody) {
  tbody.innerHTML = ''; // 테이블을 초기화
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
      `;
      tbody.appendChild(row);
  });
}

// 페이지가 로드되면 사용자 정보를 업데이트
updateUserInfo();

  // 로그아웃 버튼 클릭 이벤트
  logoutButton.addEventListener('click', () => {
    // 사용자에게 로그아웃 알림
    alert('로그아웃 되었습니다.');

    // 로그아웃 요청
    fetch('/logout', {
      method: 'POST',
    })
      .then((response) => {
        if (response.ok) {
          // 로그아웃 성공 시 /login으로 리다이렉트
          window.location.href = '/';
        } else {
          alert('로그아웃 중 오류가 발생했습니다.'); // 오류 메시지 표시
        }
      })
      .catch((error) => {
        console.error('Error:', error); // 콘솔에 오류 로그
      });
  });

  // 초기화
  displayIssues();
