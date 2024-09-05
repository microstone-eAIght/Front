document.addEventListener('DOMContentLoaded', () => {
  const cctvVideo1 = document.getElementById('cctvVideo1');
  const cctvVideo2 = document.getElementById('cctvVideo2');
  const cctvVideo3 = document.getElementById('cctvVideo3');
  const cctvVideo4 = document.getElementById('cctvVideo4');
  const logoutButton = document.getElementById('logoutButton');

  // 사용자 정보를 저장하는 예제 객체 (실제로는 서버에서 받아와야 함)
  const user = {
    name: '홍길동님',
    notifications: 3,
  };

  // 사용자 이름과 알림 수를 업데이트하는 함수
  function updateUserInfo() {
    const userNameElement = document.getElementById('userName');
    const notificationCountElement =
      document.getElementById('notificationCount');

    userNameElement.textContent = user.name;
    notificationCountElement.textContent = user.notifications;
  }

  // 페이지가 로드되면 사용자 정보를 업데이트
  updateUserInfo();

  // CCTV 영상 소스 설정 (실제 소스를 여기에 설정하세요)
  cctvVideo1.src = 'path_to_cctv_stream1';
  cctvVideo2.src = 'path_to_cctv_stream2';
  cctvVideo3.src = 'path_to_cctv_stream3';
  cctvVideo4.src = 'path_to_cctv_stream4';

  // 로그아웃 버튼 클릭 이벤트
  logoutButton.addEventListener('click', () => {
    alert('로그아웃 되었습니다.');
    // 실제 로그아웃 로직을 여기에 추가하세요
  });

  // 초기화
  displayIssues();

  // 더블클릭 및 마우스 오버 기능 추가
  const cctvs = document.querySelectorAll('.cctv');

  cctvs.forEach((cctv) => {
    // 더블클릭 이벤트 핸들러
    cctv.addEventListener('dblclick', () => {
      const isFullScreen = cctv.classList.contains('full-screen');
      cctvs.forEach((c) => c.classList.remove('full-screen'));
      if (!isFullScreen) {
        cctv.classList.add('full-screen');
      }
    });

    // 마우스를 올렸을 때 스타일 변경
    cctv.addEventListener('mouseover', () => {
      cctv.style.border = '2px solid yellow';
      cctv.style.cursor = 'pointer';
    });

    // 마우스가 떠났을 때 스타일 원래대로
    cctv.addEventListener('mouseout', () => {
      cctv.style.border = '';
      cctv.style.cursor = '';
    });
  });
});

function openWorkshopWindow(workshopNumber, workshopName, cctvStream) {
  // 현재 창의 크기를 가져옴
  let width = window.innerWidth;
  let height = window.innerHeight;

  // 새로운 창의 크기를 현재 창보다 100px 작게 설정
  let newWidth = width - 100;
  let newHeight = height - 100;

  // 창 옵션 설정
  let windowFeatures = `width=${newWidth},height=${newHeight},top=50,left=50`;

  // 새 창 열기
  let newWindow = window.open('', `작업장${workshopNumber}`, windowFeatures);

  // 새 창에 내용 삽입
  newWindow.document.open();
  newWindow.document.write(`
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>작업장${workshopName}</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

        </head>
        <body class="new-window-body">
            <header class="new-window-header">
                <h1>작업현장 영상 수집 데이터</h1>
            </header>
            <main class="new-window-main-content">
                <aside class="new-window-sidebar">
                    <h2>작업장: 작업장${workshopName}</h2>
                    <button>WorkingHours</button>
                    <button>RULA</button>
                    <button>REBA</button>
                    <button>OWAS</button>
                    <button>REPORT</button>
                </aside>
                <section class="cctv-section">
                    <div class="cctv-container">
                        <div class="cctv" id="cctv1"></div>
                        <div class="cctv" id="cctv2"></div>
                        <div class="cctv" id="cctv3"></div>
                        <div class="cctv" id="cctv4"></div>
                    </div>

                    <div class="new-window-footer">
                        <p>© 작업장 데이터 수집 시스템</p>
                    </div>
                </section>
                <aside class="evaluation-sidebar">
                    <div class="evaluation-category">
                        <h3>Neck</h3>
                        <p>(2) Neck Bend : 45° (Front)</p>
                        <p>(1) Neck Twist : 30° (Left)</p>
                        <p>(3) Neck Side-bend : 25° (Right)</p>
                    </div>
                    <div class="evaluation-category">
                        <h3>Trunk</h3>
                        <p>(2) Trunk Bend : 60° (Front)</p>
                        <p>(1) Trunk Twist : 40° (Left)</p>
                        <p>(3) Trunk Side-bend : 30° (Right)</p>
                    </div>
                    <div class="evaluation-category">
                        <h3>Legs</h3>
                        <p>(2) Leg Posture : Standing</p>
                        <p>(1) Leg Support : Weight on one leg</p>
                        <p>(3) Leg Movement : Walking</p>
                    </div>
                    <div class="evaluation-category">
                        <h3>Upper Arm</h3>
                        <p>(2) Upper Arm Lift : 90°</p>
                        <p>(1) Upper Arm Reach : 70°</p>
                        <p>(3) Upper Arm Twist : 50°</p>
                    </div>
                    <div class="evaluation-category">
                        <h3>Forearm</h3>
                        <p>(2) Forearm Rotation : 45° (Pronation)</p>
                        <p>(1) Forearm Lift : 60°</p>
                        <p>(3) Forearm Reach : 70°</p>
                    </div>
                    <div class="evaluation-category">
                        <h3>Wrist</h3>
                        <p>(2) Wrist Flexion/Extension : 30°</p>
                        <p>(1) Wrist Deviation : 20°</p>
                        <p>(3) Wrist Rotation : 40°</p>
                    </div>
                    <div class="evaluation-category">
                        <h3>Hand</h3>
                        <p>(2) Hand Grip : Strength 5</p>
                        <p>(1) Hand Dexterity : Fine movements</p>
                        <p>(3) Hand Posture : Open</p>
                    </div>
                    <div class="evaluation-category">
                        <h3>Shoulder</hge>
                        <p>(2) Shoulder Lift : 90°</p>
                        <p>(1) Shoulder Abduction/Adduction : 70°</p>
                        <p>(3) Shoulder Rotation : 60°</p>
                    </div>
                    <div class="evaluation-category">
                        <h3>Back</h3>
                        <p>(2) Back Bend : 50°</p>
                        <p>(1) Back Twist : 40°</p>
                        <p>(3) Back Load : 15kg</p>
                    </div>
                </aside>
                <aside class="empty-sidebar">
                    <!-- 빈 바 -->
                </aside>
            </main>
        </body>
        <script src="{{ url_for('static', filename='cctvZoom.js') }}"></script>
        </html>
    `);
  newWindow.document.close();
}
