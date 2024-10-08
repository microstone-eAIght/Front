let imgname; // 전역 변수로 이미지 이름 저장

document.addEventListener('DOMContentLoaded', function () {
    let tabContainer = document.createElement('div');
    tabContainer.classList.add('tab-container');
    document.querySelector('.analysis-video').prepend(tabContainer);

    let tabs = [];

    document.querySelectorAll('.analysis-item').forEach((item, index) => {
        item.addEventListener('dblclick', function () {
            let imgSrc = this.querySelector('img').src; // 이미지 경로 추출
            let videoArea = document.querySelector('.analysis-images'); // 이미지를 표시할 영역

            // 탭이 이미 존재하는지 확인
            let existingTab = tabs.find(tab => tab.imgSrc === imgSrc);
            if (!existingTab) {
                // 새 탭 추가
                let newTab = document.createElement('div');
                newTab.classList.add('tab');
                newTab.textContent = `Tab ${tabs.length + 1}`;
                let closeButton = document.createElement('span');
                closeButton.innerHTML = '&times;';
                closeButton.classList.add('close-btn');
                newTab.appendChild(closeButton);

                // 탭 클릭 시 해당 이미지로 이동
                newTab.addEventListener('click', function () {
                    videoArea.querySelector('img').src = imgSrc;
                    highlightTab(newTab);
                });

                // 탭 닫기 기능
                closeButton.addEventListener('click', function (e) {
                    e.stopPropagation();
                    tabContainer.removeChild(newTab);
                    tabs = tabs.filter(tab => tab.element !== newTab);
                    if (tabs.length > 0) {
                        videoArea.querySelector('img').src = tabs[tabs.length - 1].imgSrc;
                        highlightTab(tabs[tabs.length - 1].element);
                    } else {
                        videoArea.innerHTML = ''; // 모든 탭이 닫히면 이미지 제거
                    }
                });

                tabContainer.appendChild(newTab);
                tabs.push({ element: newTab, imgSrc: imgSrc });

                // 이미지를 표시할 영역에 이미지 추가
                if (!videoArea.querySelector('img')) {
                    let newImg = document.createElement('img');
                    newImg.src = imgSrc;
                    videoArea.appendChild(newImg);
                } else {
                    videoArea.querySelector('img').src = imgSrc;
                }
                highlightTab(newTab);
            } else {
                // 탭이 이미 존재할 경우 해당 이미지를 다시 출력
                videoArea.querySelector('img').src = imgSrc;
                highlightTab(existingTab.element);
            }
        });
    });

    function highlightTab(tab) {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active-tab'));
        tab.classList.add('active-tab');
    }
});

function selectImage(id) {
    fetch('/get_recent_images')  // 서버에서 최신 이미지를 가져옴
        .then(response => response.json())
        .then(data => {
            const latestImage = data.latest_image; // 최신 이미지 파일 이름
            const imageElement = document.getElementById(`image${id}`);
            const placeholder = document.getElementById(`placeholder${id}`);
            const deleteButton = document.querySelector(`.analysis-list${id} .delete-button`);

            if (latestImage) {
                imageElement.src = `http://127.0.0.1:5000/high_risk_images/${latestImage}`;
                imageElement.style.display = 'block';  // 이미지 표시
                placeholder.style.display = 'none';  // "Add Image" 텍스트 숨기기
                deleteButton.style.display = 'inline-block';  // 삭제 버튼 보이기
            }
        })
        .catch(error => {
            console.error('이미지 불러오기 오류:', error);
        });
}

function openFolder(id) {
    const imageElement = document.getElementById(`image${id}`);
    const placeholder = document.getElementById(`placeholder${id}`);
    const deleteButton = document.querySelector(`.analysis-list${id} .delete-button`);

    // null 체크 추가
    if (imageElement && placeholder && deleteButton) {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*'; // 이미지 파일만 선택 가능

        input.onchange = event => {
            const file = event.target.files[0]; // 선택된 파일 가져오기
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    imageElement.src = e.target.result;  // 선택된 이미지로 변경
                    imageElement.style.display = 'block';  // 이미지 보이기
                    placeholder.style.display = 'none';  // "Add Image" 텍스트 숨기기
                    deleteButton.style.display = 'inline-block';  // 삭제 버튼 보이기

                    imgname = file.name; // 이미지 이름을 전역 변수에 저장
                    console.log(`Selected image name: ${imgname}`); // 선택된 이미지 이름 로그
                };
                reader.readAsDataURL(file); // 이미지 파일을 base64로 변환하여 미리보기 가능하게 함
            }
        };

        input.click(); // 파일 선택창 열기
    } else {
        console.error(`해당 ID로 요소를 찾을 수 없습니다: image${id}`);
    }
}

// 이미지 삭제 (이미지를 숨기고 빈 상태로 만듦)
function removeImage(id) {
    const imageElement = document.getElementById(`image${id}`);
    const placeholder = document.getElementById(`placeholder${id}`);
    const deleteButton = document.querySelector(`.analysis-list${id} .delete-button`);

    if (imageElement && placeholder && deleteButton) {
        imageElement.style.display = 'none';  // 이미지 숨기기
        imageElement.src = '';  // 이미지 경로 초기화 (아무것도 표시되지 않도록)
        placeholder.style.display = 'flex';  // "Add Image" 텍스트 보이기
        deleteButton.style.display = 'block';  // 삭제 
    } else {
        console.error("해당 ID로 요소를 찾을 수 없습니다.");
    }
}

// 폴더에서 이미지 가져오기 및 버튼 기능 연결
document.getElementById('folder-button').addEventListener('click', function () {
    // 서버에서 최근 이미지 10개를 가져옴
    fetch('/get_recent_images')  // Flask API에 요청
        .then(response => response.json())
        .then(data => {
            const imageUrls = data.images.map(img => `http://127.0.0.1:5000/high_risk_images/${img}`);
            const analysisItems = document.querySelectorAll('.analysis-list .analysis-item img');
            for (let i = 0; i < imageUrls.length && i < analysisItems.length; i++) {
                analysisItems[i].src = imageUrls[i];  // 이미지 소스를 새로 설정
                analysisItems[i].style.display = 'block';  // 이미지 보이기
                document.getElementById(`placeholder${i+1}`).style.display = 'none';  // "Add Image" 텍스트 숨기기
            }
        })
        .catch(error => console.error('이미지 불러오기 오류:', error));
});

document.addEventListener('DOMContentLoaded', function () {
    const defaultImageSrc = "http://127.0.0.1:5000/high_risk_images/default.jpg";  // 기본 이미지 경로

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
});
