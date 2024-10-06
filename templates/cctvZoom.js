document.addEventListener('DOMContentLoaded', () => {
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
});
