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
