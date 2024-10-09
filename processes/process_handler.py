# signal_handler.py
import signal
import sys
from processes.process_manager import stop_all_scripts

# SIGINT 핸들러 설정
def signal_handler(sig, frame):
    stop_all_scripts()  # 모든 스크립트를 종료
    print("스크립트 전부 종료")
    sys.exit(0)

# 시그널 핸들러 등록
def register_signal_handlers():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
