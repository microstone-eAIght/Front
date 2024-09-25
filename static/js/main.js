// 첫 화면에서 웹캠 스트림과 녹화를 시작하는 함수
function startWebcamAndRecording() {
  const videoElement = document.getElementById('cctvVideo1');
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true }).then(function (mediaStream) {
          videoElement.srcObject = mediaStream;
          videoElement.play();
          startRecording(mediaStream); // 녹화 자동 시작
      }).catch(function(error) {
          console.error("웹캠 시작 중 오류 발생:", error);
      });
  }
}

// 녹화 시작 함수
function startRecording(stream) {
  let mediaRecorder = new MediaRecorder(stream);
  let recordedChunks = [];
  let recordingInterval;

  mediaRecorder.ondataavailable = event => {
      if (event.data.size > 0) {
          recordedChunks.push(event.data);
      }
  };

  mediaRecorder.onstop = () => {
      // 저장된 데이터로 파일 생성 및 다운로드
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      link.download = `recorded_video_${timestamp}.webm`;
      link.click();

      // 녹화 데이터 초기화
      recordedChunks = [];

      // 녹화 다시 시작
      mediaRecorder.start();
  };

  mediaRecorder.start();

  // 주기적으로 녹화 중지
  recordingInterval = setInterval(() => {
      mediaRecorder.stop();
  }, 5000); // 5초마다 녹화 중지
}

// 창이 로드될 때 웹캠을 시작하고 녹화도 시작
window.onload = function() {
  startWebcamAndRecording();
};

const logoutButton = document.getElementById('logoutButton');

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

function openWorkshopWindow(workshopNumber, workshopName, cctvStreams) {
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
      <link rel="stylesheet" href="/static/style.css">
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
                  <video id="cctvVideo1" class="cctv" autoplay></video>
                  <video id="cctvVideo2" class="cctv" autoplay></video>
                  <video id="cctvVideo3" class="cctv" autoplay></video>
                  <video id="cctvVideo4" class="cctv" autoplay></video>
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
                    <h3>Shoulder</h3>
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
      </main>
      <script about="recording">
        let mediaRecorder;
        let recordedChunks = [];
        let recordingInterval;
        let stream;

        // 웹캠 스트림을 자동으로 시작하는 함수
        function startWebcam() {
          const videoElement = document.getElementById('cctvVideo1');
          if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true }).then(function (mediaStream) {
              videoElement.srcObject = mediaStream;
              videoElement.play();
              stream = mediaStream; // 스트림 저장
              startRecording(); // 녹화 자동 시작
            }).catch(function(error) {
              console.error("웹캠 시작 중 오류 발생:", error);
            });
          }
        }

        // 녹화 시작
        function startRecording() {
          mediaRecorder = new MediaRecorder(stream);

          mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
              recordedChunks.push(event.data);
            }
          };

          mediaRecorder.onstop = () => {
            // 저장된 데이터로 파일 생성 및 다운로드
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            link.download = \`recorded_video_\${timestamp}.webm\`;
            link.click();

            // 녹화 데이터 초기화
            recordedChunks = [];

            // 녹화 다시 시작
            mediaRecorder.start();
          };

          mediaRecorder.start();

          // 주기적으로 녹화 중지
          recordingInterval = setInterval(() => {
            mediaRecorder.stop();
          }, 5000); // 5초마다 녹화 중지
        }

        // 녹화 중지
        function stopRecording() {
          clearInterval(recordingInterval);
          if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
          }
        }

        // 창이 열리면 자동으로 웹캠 시작 및 녹화
        window.onload = function() {
          startWebcam();
          initializeCCTVZoom();
        };

        // CCTV 줌 기능 초기화
        function initializeCCTVZoom() {
          const cctvs = document.querySelectorAll('.cctv');

          cctvs.forEach(cctv => {
            // 더블클릭 이벤트 핸들러
            cctv.addEventListener('dblclick', () => {
              const isFullScreen = cctv.classList.contains('full-screen');
              cctvs.forEach(c => c.classList.remove('full-screen'));
              if (!isFullScreen) {
                cctv.classList.add('full-screen');
              }
            });

            // 마우스를 올렸을 때 스타일 변경
            cctv.addEventListener('mouseover', () => {
              cctv.style.border = '2px solid red';
              cctv.style.cursor = 'pointer';
            });

            // 마우스가 떠났을 때 스타일 원래대로
            cctv.addEventListener('mouseout', () => {
              cctv.style.border = '';
              cctv.style.cursor = '';
            });
          });
        }
      </script>
  </body>
  </html>
  `);
  newWindow.document.close();
}
