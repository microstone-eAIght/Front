function loadRebaA() {
    fetch('/reba_a')
        .then(response => response.json())
        .then(data => {
            const rebaPlot = document.getElementById('reba-plot');
            rebaPlot.innerHTML = data.graph_html;

            // 동적으로 삽입된 <script> 태그 실행
            const scripts = rebaPlot.getElementsByTagName('script');
            for (let i = 0; i < scripts.length; i++) {
                const script = document.createElement('script');
                script.text = scripts[i].text;
                document.body.appendChild(script);
            }

            // REBA A SCORE 표시
            const levelInfo = document.getElementById('level-info');
            levelInfo.innerHTML = `REBA A SCORE: <strong>${data.score_a}</strong>`;
        })
        .catch(error => console.error('Error loading REBA A:', error));
}

function loadRebaB() {
    fetch('/reba_b')
        .then(response => response.json())
        .then(data => {
            const rebaPlot = document.getElementById('reba-plot');
            rebaPlot.innerHTML = data.graph_html;

            // 동적으로 삽입된 <script> 태그 실행
            const scripts = rebaPlot.getElementsByTagName('script');
            for (let i = 0; i < scripts.length; i++) {
                const script = document.createElement('script');
                script.text = scripts[i].text;
                document.body.appendChild(script);
            }

            // REBA B SCORE 표시
            const levelInfo = document.getElementById('level-info');
            levelInfo.innerHTML = `REBA B SCORE: <strong>${data.score_b}</strong>`;
        })
        .catch(error => console.error('Error loading REBA B:', error));
}

function loadRebaC() {
    fetch('/reba_c')
        .then(response => response.json())
        .then(data => {
            const rebaPlot = document.getElementById('reba-plot');
            const figData = data.fig_data;

            // REBA C 게이지 차트 표시
            Plotly.newPlot(rebaPlot, figData.data, figData.layout).then(() => {
                // 애니메이션 추가
                animateGauge(rebaPlot, 0, data.score_c); // 0에서 score_c까지 차오르게
            });

            // REBA C SCORE 및 Risk Level 표시
            const levelInfo = document.getElementById('level-info');
            levelInfo.innerHTML = `
                <strong>
                    REBA C SCORE: <span style="color: ${data.color};">${data.score_c}</span><br>
                    Risk Level: <span style="color: ${data.color};">${data.risk_level}</span>
                </strong>
            `;
        })
        .catch(error => console.error('Error loading REBA C:', error));
}

// 게이지 애니메이션 함수
function animateGauge(gaugeElement, startValue, endValue) {
    let currentValue = startValue;
    const duration = 1000;  // 애니메이션 지속 시간 (1초)
    const intervalTime = 10;  // 업데이트 간격 (밀리초)
    const step = (endValue - startValue) / (duration / intervalTime);

    const interval = setInterval(() => {
        currentValue += step;
        if (currentValue >= endValue) {
            currentValue = endValue;
            clearInterval(interval);
        }

        // Plotly로 게이지 값을 업데이트
        Plotly.update(gaugeElement, {
            'value': [currentValue],
            'gauge.threshold.value': currentValue  // threshold 값도 변경
        });
    }, intervalTime);
}

function loadAllScores() {
    fetch('/all_scores')
        .then(response => response.json())
        .then(data => {
            // REBA A, B, C 점수 및 결합된 위험도를 표시하는 부분
            const levelInfo = document.getElementById('level-info');
            levelInfo.innerHTML = `
    <strong>
        REBA A SCORE: ${data.score_a}<br>
        REBA B SCORE: ${data.score_b}<br>
        REBA C SCORE: <span style="color: ${getScoreColor(data.score_c)};">${data.score_c}</span><br>
        Risk of A and B Combined: <span style="color: ${getRiskColor(data.combined_risk)};">${data.combined_risk}</span>
    </strong>
`;

            // REBA C 게이지 차트 표시
            const rebaPlot = document.getElementById('reba-plot');
            const figData = data.fig_data;

            // Plotly로 게이지 차트 렌더링
            Plotly.newPlot(rebaPlot, figData.data, figData.layout);
        })
        .catch(error => console.error('Error loading all scores:', error));
}

// REBA C 점수에 따른 색상 반환 함수
function getScoreColor(score) {
    if (score <= 3) {
        return 'green';
    } else if (score <= 6) {
        return 'yellow';
    } else if (score <= 9) {
        return 'orange';
    } else {
        return 'red';
    }
}

// Risk of A and B Combined 위험도에 따른 색상 반환 함수
function getRiskColor(risk) {
    switch (risk) {
        case 'Low Risk':
            return 'lightgreen';
        case 'Medium Risk':
            return 'yellow';
        case 'High Risk':
            return 'orange';
        case 'Very High Risk':
            return 'red';
        default:
            return 'green';  // 기본값 (Normal Risk)
    }
}




function loadOwasChart() {
    fetch('/owas_chart')
        .then(response => response.json())
        .then(data => {
            const owasPlot = document.getElementById('owas-plot');
            
            // OWAS 그래프를 렌더링
            Plotly.newPlot(owasPlot, data.fig_data.data, data.fig_data.layout);

            // OWAS 위험도에 따른 텍스트 색상 변경
            const owasLevelInfo = document.getElementById('owas-level-info');
            let riskColor;
            
            switch (data.owas_level) {
                case "Normal risk":
                    riskColor = "green";
                    break;
                case "Low risk":
                    riskColor = "lightgreen";
                    break;
                case "Medium risk":
                    riskColor = "orange";
                    break;
                case "High risk":
                    riskColor = "red";
                    break;
                default:
                    riskColor = "black";  // 기본 색상 설정
            }

            // OWAS 레벨 정보 업데이트 및 색상 반영 (OWAS Level은 기본색, 위험도만 색상 반영)
            owasLevelInfo.innerHTML = `OWAS Level: <strong style="color: ${riskColor};">${data.owas_level}</strong>`;
        })
        .catch(error => console.error('Error loading OWAS chart:', error));
}



function selectImage(id) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*'; // 이미지 파일만 허용

    input.onchange = event => {
        const file = event.target.files[0]; // 선택된 파일 가져오기
        if (file) {
            const imgname = file.name; // 파일 이름 추출
            console.log(`선택된 이미지 이름: ${imgname}`);
            document.getElementById('imgnameInput').value = imgname; // HTML 요소에 저장
            
            // 이미지 경로 전송
            const formData = new FormData();
            formData.append('imgname', imgname); // 이미지 이름을 추가
            
            // AJAX 요청으로 서버에 전송
            fetch('/your-flask-route', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); // 서버 응답 처리
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    };

    input.click(); // 파일 선택기 열기
}



function openFolder(id, imageSrc) {
    const imageElement = document.getElementById(`image${id}`);
    const placeholder = document.getElementById(`placeholder${id}`);
    const selectedText = document.getElementById(`selected-text${id}`);
    const deleteButton = document.querySelector(`.analysis-list${id} .delete-button`);

    // 이미지가 선택되면
    if (imageSrc) {
        placeholder.style.display = 'none';  // "Add Image" 텍스트 숨기기
        selectedText.style.display = 'none';  // "Selected Image" 텍스트 숨기기
        imageElement.src = imageSrc;  // 선택된 이미지 경로 설정
        imageElement.style.display = 'block';  // 이미지 보이기
        deleteButton.style.display = 'inline-block';  // 삭제 버튼 보이기
    } else {
        // 이미지가 선택되지 않으면
        placeholder.style.display = 'flex';  // "Add Image" 텍스트 보이기
        selectedText.style.display = 'block';  // "Selected Image" 텍스트 숨기기
        imageElement.style.display = 'none';  // 이미지 숨기기
    }
}

// 이미지 삭제
function removeImage(id) {
    const imageElement = document.getElementById(`image${id}`);
    const placeholder = document.getElementById(`placeholder${id}`);
    const selectedText = document.getElementById(`selected-text${id}`);
    const deleteButton = document.querySelector(`.analysis-list${id} .delete-button`);

    // 이미지와 관련된 요소 상태 초기화
    imageElement.style.display = 'none';  // 이미지 숨기기
    imageElement.src = '';  // 이미지 경로 초기화
    selectedText.style.display = 'none';  // "Selected Image" 텍스트 숨기기
    placeholder.style.display = 'flex';  // "Add Image" 텍스트 보이기
    deleteButton.style.display = 'none';  // 삭제 버튼 숨기기
}

// 폴더에서 이미지 가져오기 및 버튼 기능 연결
document.getElementById('folder-button').addEventListener('click', function () {
    // 서버에서 최근 이미지 10개를 가져옴
    fetch('/get_recent_images')
        .then(response => response.json())
        .then(data => {
            const imageUrls = data.images;
            const analysisItems = document.querySelectorAll('.analysis-list .analysis-item img');
            for (let i = 0; i < imageUrls.length && i < analysisItems.length; i++) {
                analysisItems[i].src = imageUrls[i];  // 이미지 소스를 새로 설정
                analysisItems[i].style.display = 'block';  // 이미지 보이기
                document.getElementById(`placeholder${i+1}`).style.display = 'none';  // 텍스트 숨기기
            }
        })
        .catch(error => console.error('이미지 불러오기 오류:', error));
});

document.addEventListener('DOMContentLoaded', function () {
    const defaultImageSrc = "{{ url_for('static', filename='img/default.png') }}";  // 기본 이미지 경로

    // 'x' 버튼 클릭 시 기본 이미지로 변경
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function () {
            const analysisItem = this.closest('.analysis-item');
            const imgElement = analysisItem.querySelector('img');
            imgElement.src = defaultImageSrc;  // 기본 이미지로 변경
            imgElement.style.display = 'none';  // 이미지 숨기기
            const placeholder = analysisItem.querySelector('.image-placeholder');
            placeholder.style.display = 'flex';  // Add Image 텍스트 보이기
        });
    });

    // '+' 버튼 클릭 시 파일 선택 및 이미지 변경
    document.querySelectorAll('.add-button').forEach(button => {
        button.addEventListener('click', function () {
            const analysisItem = this.closest('.analysis-item');
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';

            // 파일 선택 후 이미지 변경
            input.addEventListener('change', function (event) {
                const file = event.target.files[0];
                const placeholder = analysisItem.querySelector('.image-placeholder');
                const imgElement = analysisItem.querySelector('img');
                
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        imgElement.src = e.target.result;  // 선택된 이미지로 변경
                        imgElement.style.display = 'block';  // 이미지 표시
                        placeholder.style.display = 'none';  // Add Image 텍스트 숨기기
                    };
                    reader.readAsDataURL(file);
                } else {
                    // 파일이 선택되지 않았을 경우 placeholder 복구
                    placeholder.style.display = 'flex';  // Add Image 텍스트 다시 보이기
                    imgElement.style.display = 'none';   // 이미지 숨기기
                }
            });

            // 새로운 이미지를 추가하려고 했을 때 placeholder를 다시 설정
            const imgElement = analysisItem.querySelector('img');
            const placeholder = analysisItem.querySelector('.image-placeholder');

            if (imgElement.src && imgElement.src !== defaultImageSrc) {
                // 이미지가 이미 있는 상태라면 Add Image 텍스트를 숨겨둠
                placeholder.style.display = 'none';
            }

            input.click();  // 파일 선택창 열기
        });
    });
});
