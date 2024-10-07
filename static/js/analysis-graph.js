function loadRebaA() {
    const frameTitle = imgname; // imgname이 frame_title에 해당하는지 확인

    if (frameTitle) {
        fetch(`/reba_a?frame_title=${encodeURIComponent(frameTitle)}`)
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
    } else {
        console.error('No image selected. Please select an image first.');
    }
}

function loadRebaB() {
    const frameTitle = imgname; // imgname이 frame_title에 해당하는지 확인

    if (frameTitle) {
        fetch(`/reba_b?frame_title=${encodeURIComponent(frameTitle)}`)
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
    } else {
        console.error('No image selected. Please select an image first.');
    }
}


function loadRebaC() {
    const frameTitle = imgname; // imgname을 사용하여 frame_title 설정

    if (frameTitle) {
        fetch(`/reba_c?frame_title=${encodeURIComponent(frameTitle)}`) // frame_title을 포함하여 요청
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
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
    } else {
        console.error('No image selected. Please select an image first.'); // 이미지가 선택되지 않았을 때 경고 메시지
    }
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
    const frameTitle = imgname; // imgname이 현재 선택된 이미지의 이름이라고 가정

    fetch(`/all_scores?frame_title=${encodeURIComponent(frameTitle)}`) // frame_title을 쿼리 파라미터로 전달
        .then(response => response.json())
        .then(data => {
            // REBA A, B, C 점수 및 결합된 위험도를 표시하는 부분
            const levelInfo = document.getElementById('level-info');
            levelInfo.innerHTML = `
                <strong>
                    REBA A SCORE: <span style="color: ${getScoreColor(data.score_a)};">${data.score_a}</span><br>
                    REBA B SCORE: <span style="color: ${getScoreColor(data.score_b)};">${data.score_b}</span><br>
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
    const frameTitle = imgname; // imgname이 현재 선택된 이미지의 이름이라고 가정

    fetch(`/owas_chart?frame_title=${encodeURIComponent(frameTitle)}`) // frame_title을 쿼리 파라미터로 전달
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




