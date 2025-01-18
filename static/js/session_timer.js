// session_timer.js

// 獲取超時時間（從 HTML 的 data-* 屬性）
const scriptElement = document.querySelector('script[src$="session_timer.js"]');
const timeoutMinutes = parseInt(scriptElement.getAttribute('data-timeout-minutes'), 10) || 5;

// 初始化倒數時間
let remainingTime = timeoutMinutes * 60; // 秒數計算
const timerDisplay = document.getElementById('timer-display');
const resetTimerBtn = document.getElementById('reset-timer-btn');

// 更新倒數計時器顯示
function updateTimerDisplay() {
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    timerDisplay.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// 每秒減少倒數時間，並使用同步方法計算剩餘時間
let lastTimestamp = Date.now();
const countdownInterval = setInterval(() => {
    const now = Date.now();
    const elapsed = Math.floor((now - lastTimestamp) / 1000);
    if (elapsed > 0) {
        remainingTime -= elapsed;
        lastTimestamp = now;
        if (remainingTime <= 0) {
            clearInterval(countdownInterval);
            alert('您的會話已過期，請重新登入。');
            window.location.href = '/logout/';
            return;
        }
        updateTimerDisplay();
    }
}, 1000);

// 重新計時功能
resetTimerBtn.addEventListener('click', () => {
    fetch('/reset-timer/', { method: 'GET' })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            remainingTime = timeoutMinutes * 60; // 重置倒數時間
            lastTimestamp = Date.now();
            updateTimerDisplay();
            alert('計時器已重新設置！');
        })
        .catch((err) => {
            console.error('Failed to reset timer:', err);
            alert('計時器重新設置失敗，請稍後再試。');
        });
});

// 初始化顯示
updateTimerDisplay();
