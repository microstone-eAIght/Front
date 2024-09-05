body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f0f0f0;
}

.container {
    display: flex;
    height: 100vh;
    background-color: #212121;
}


.workshop-container{
    background-color: #212121;
    padding-top: 40px;
    padding-bottom:1px;
    margin-bottom:1px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
    margin-left: 0;
    width: 100%;
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
}

.workshop {
    background-color: #007BFF;
    padding: 20px;
    border-radius: 4px;
    text-align: center;
    font-weight: bold;
    flex: 0 0 200px;
    margin: 0 3px;
    color:white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
    transition: background-color 0.3s ease, transform 0.3s ease; 
}
.workshop:hover {
    background-color: #0056b3;
    transform: translateY(-5px);
}

.sidebar {
    width: 200px;
    background-color: #007BFF;
    padding-top: 20px;
    border-right: 1px solid #ccc;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.sidebar ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

.sidebar ul li {
    margin: 10px 0;
    border-bottom: 1px solid #0056b3;
}

.sidebar ul li a {
    color: white;
    text-decoration: none;
    display: block;
    padding: 10px 20px;
    border-radius: 4px;
}

.sidebar ul li a:hover {
    background-color: #0056b3;
}

#logoutButton {
    margin: 20px;
    padding: 10px;
    background-color: #0056b3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

#logoutButton:hover {
    background-color: #0056b3;
}

.main-content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
}

.main-header {
    background-color: #007BFF;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    margin-bottom: 20px;
    text-align: center;
}

.system-title {
    margin: 0;
}

.content {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.cctv-stream {
    width: 100%;
    background-color: #212121;
    padding: 1px;
    border-radius: 4px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    margin-top:1px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
}

.cctv-stream video {
    width: 100%;
    border-radius: 4px;
    border: 1px solid #ccc;
}

.user-info {
    display: flex;
    justify-content: center; /* 수평으로 중앙 정렬 */
    align-items: center; /* 수직으로 중앙 정렬 */
    color: white;
}

.notification-button {
    background-color: #0056b3; /* 알림 버튼 색상 */
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px;
    margin: 10px;
    cursor: pointer;
    position: relative; /* 알림 카운트 위치를 조정하기 위해 필요 */
}

.notification-count {
    background-color: red; /* 알림 카운트 배경 색상 */
    color: white;
    border-radius: 50%;
    padding: 5px 10px;
    position: absolute;
    top: -10px;
    right: -10px;
    font-size: 12px;
    font-weight: bold;
}


/* 전체 레이아웃 스타일 */
.new-window-body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    width: 100vw;
    height: 100vh;
    background-color: #f0f0f0;
}

.new-window-header,
.new-window-footer {
    width: 100%;
    padding: 10px;
    background-color: #212121;
    color:white;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-bottom: 1px solid #ccc;
}

.new-window-footer {
    color:white;
    border-top: 1px solid #ccc;
}

.new-window-header h1,
.new-window-footer p {
    margin: 0;
    font-size: 1rem;
}
/* 맨 아래 가로 바 스타일 */
.new-window-footer {
    width: 100%;
    padding: 10px;
    background-color: #212121;
    color:white;
    text-align: center;
    box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
    border-top: 1px solid #ccc;
    margin-top: 10px;
    flex-shrink: 0; /* 부모 요소의 크기에 맞춰지지 않도록 고정 */
}

.new-window-main-content {
    display: flex;
    flex-grow: 1; /* 남은 공간을 자동으로 채움 */
    width: 100%;
    height:70%;
    background-color: #fff;
}

.new-window-sidebar,
.evaluation-sidebar,
.empty-sidebar {
    width: 15%;
    padding: 10px;
    background-color: #212121;
    color:white;
    overflow-y: auto;
    font-size: 0.5rem;
    border-left: 1px solid #ccc;
}

.evaluation-sidebar {
    width: 20%; /* 평가 요소 바의 가로 길이를 늘림 */
}

.cctv-section {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
    background-color: #212121;
    color:white;
    
}

.new-window-cctv-stream {
    width: 100%;
    height: calc(100% - 40px);
    background-color: #212121;
    padding: 1px;
    border-radius: 4px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 10px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 5px;
}

.new-window-cctv-stream video {
    width: 100%;
    height: 100%;
    background-color: black;
}

.new-window-sidebar h2{
    font-size:1rem;
    
}
.evaluation-sidebar h3 {
    margin-top: 0;
    font-size:1rem;
    
}

.new-window-sidebar button{
    background-color: #3488e2;
    color:white;
    font-size:0.7rem;
    display: block;
    width: 100%;
    margin-bottom: 5px;
}
.evaluation-sidebar p {
    background-color: black;
    font-size:0.7rem;
    display: block;
    width: 100%;
    margin-bottom: 5px;
}

.evaluation-category {
    margin-bottom: 10px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 5px;
}


/* 반응형 스타일 */
@media (max-width: 1200px) {
    .new-window-header h1, .new-window-footer p {
        font-size: 0.9rem;
    }

    .new-window-sidebar, .evaluation-sidebar, .empty-sidebar {
        font-size: 0.6rem;
    }
}

@media (max-width: 768px) {
    .new-window-header h1, .new-window-footer p {
        font-size: 0.8rem;
    }

    .new-window-sidebar, .evaluation-sidebar, .empty-sidebar {
        font-size: 0.5rem;
        width:20%;
    }
}

@media (max-width: 480px) {
    .new-window-header h1, .new-window-footer p {
        font-size: 0.7rem;
    }

    .new-window-sidebar, .evaluation-sidebar, .empty-sidebar {
        font-size: 0.4rem;
    }
}







.cctv-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 10px;
    width: 90%;
    height: 90vh;
    box-sizing: border-box; /* 여백과 테두리 포함하여 크기 계산 */
}

.cctv {
    width: 100%;
    height: 100%;
    background-color: #000; /* 배경색을 검정색으로 설정 */
    border-radius: 4px; /* 모서리 둥글게 */
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 살짝의 그림자 효과 */
}

.cctv:hover {
    border: 2px solid red; /* 마우스를 올렸을 때 테두리 강조 */
}

.full-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 1000;
}