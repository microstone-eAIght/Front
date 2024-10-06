import os
import shutil
import time

def get_files_from_folder(folder_path):
    """
    주어진 폴더에서 파일 목록을 반환하는 함수.
    """
    try:
        files = os.listdir(folder_path)
        return sorted(files)  # 파일 이름을 사전순으로 정렬하여 반환
    except Exception as e:
        print(f"폴더에서 파일을 가져오는 중 오류 발생: {e}")
        return []

def is_file_ready(file_path):
    """
    파일이 사용 중인지 확인하고, 사용 중이 아닐 때 True 반환.
    """
    try:
        # 파일을 열어서 읽을 수 있으면 사용 중이 아닌 것으로 간주
        with open(file_path, 'rb'):
            return True
    except:
        return False

def move_file(source, destination):
    """
    파일을 source에서 destination으로 이동하는 함수.
    """
    try:
        shutil.move(source, destination)
        print(f'{source} 파일을 {destination}로 이동했습니다.')
    except Exception as e:
        print(f'파일을 이동하는 중 오류 발생: {e}')

def move_videos_in_interval(a_folder, b_folder, interval=20):
    """
    a 폴더에서 b 폴더로 동영상을 interval(초) 간격으로 옮기는 함수.
    """
    while True:
        files = get_files_from_folder(a_folder)
        video_files = [file for file in files if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov'))]

        if video_files:
            for file_name in video_files:
                source = os.path.join(a_folder, file_name)
                destination = os.path.join(b_folder, file_name)

                # 파일이 준비된 경우에만 이동
                if is_file_ready(source):
                    move_file(source, destination)

                    # interval 초 대기
                    print(f'{interval}초 대기 중...')
                    time.sleep(interval)
                else:
                    print(f'{file_name}은(는) 아직 사용 중입니다. 나중에 다시 시도합니다.')
        else:
            # 동영상 파일이 없으면 10초마다 다시 확인
            print('동영상 파일이 없습니다. 10초 후 다시 확인합니다...')
            time.sleep(10)

# a폴더와 b폴더 경로 설정, a->b로 동영상 이동
# a_folder = 'C:/video'  # a 폴더 경로
# b_folder = 'C:/video_AI'  # b 폴더 경로

# 20초 간격으로 동영상 파일 이동 실행
move_videos_in_interval('C:/video', 'C:/video_AI', interval=20)
