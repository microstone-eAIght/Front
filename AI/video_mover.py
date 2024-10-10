import os
import shutil
import time

def get_files_from_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        return sorted(files)
    except Exception as e:
        print(f"폴더에서 파일을 가져오는 중 오류 발생: {e}")
        return []

def is_file_locked(file_path):
    """잠금 파일(.lock)이 있는지 확인"""
    lock_file_path = file_path + '.lock'
    return os.path.exists(lock_file_path)

def move_file(source, destination):
    try:
        shutil.move(source, destination)
        print(f'{source} 파일을 {destination}로 이동했습니다.')
    except Exception as e:
        print(f'파일을 이동하는 중 오류 발생: {e}')

def move_videos_in_interval(a_folder, b_folder, interval=20, lock_check_interval=5):
    """
    a 폴더에서 b 폴더로 동영상을 interval(초) 간격으로 옮기고, 
    잠금 파일이 있을 경우 lock_check_interval(초) 만큼 대기한 후 다시 시도.
    """
    while True:
        files = get_files_from_folder(a_folder)
        video_files = [file for file in files if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov'))]

        if video_files:
            for file_name in video_files:
                source = os.path.join(a_folder, file_name)
                destination = os.path.join(b_folder, file_name)

                # 잠금 파일이 없을 때만 이동
                if not is_file_locked(source):
                    move_file(source, destination)
                    print(f'{interval}초 대기 중...')
                    time.sleep(interval)
                else:
                    print(f'{file_name}은(는) 아직 잠겨 있습니다. {lock_check_interval}초 대기 후 다시 시도합니다.')
                    time.sleep(lock_check_interval)  # 잠금 파일이 있을 때 대기
        else:
            print('동영상 파일이 없습니다. 10초 후 다시 확인합니다...')
            time.sleep(10)

move_videos_in_interval('C:/video/', 'C:/video_AI/', interval=20)
