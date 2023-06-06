import sched, time
import numpy as np
import cv2 as cv
import os
#import shutil
import datetime
#import schedule
#import dropbox
#import requests
#from PIL import Image
import concurrent.futures as Executor #import Executor#, ProcessPoolExecutor as executor
import sys
import keyboard
from keyboard_wait import keyboard_wait


"""
# Check the connection between the camera numbers and the computer. 
def check_camera_connection():   
    camera_numbers = []  

    # check the camera number from 0 to 9
    for camera_number in range(10):
        cap = cv.VideoCapture(camera_number)
        ret, frame = cap.read()

        if ret is True:
            camera_numbers.append(camera_number)
            print("port number", camera_number, "Find!")

        else:
            print("port number", camera_number,"None")
    print("Connected the number of camera:", len(camera_numbers))
    return camera_numbers
"""

def operate_camera(camera_numbers, camera_format, WIDTH, HEIGHT, framerate, VIDEO=False, BUFFERSIZE=4, RAZPI=False):
    caps = {}
    camera_info = {}
    ret = []
    frame = []
    #カメラ番号ごとに以下の操作を実施
    for camera_number in camera_numbers:
        #カメラを起動
        caps[camera_number] = cv.VideoCapture(camera_number)
        #起動できなければ抜ける
        if not caps[camera_number].isOpened():
            print(f"Cannot open camera{camera_number}")
            sys.exit()
        #カメラのコーデックを指定
        caps[camera_number].set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*camera_format))#"Y", "U", "Y", "V""M", "J", "P", "G"
        #カメラの解像度(WIDTH)を指定
        caps[camera_number].set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
        #カメラの解像度(HEIGHT)を指定
        caps[camera_number].set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        #カメラのフレームレートを指定
        caps[camera_number].set(cv.CAP_PROP_FPS, framerate)
        #ラズパイを用いて動作させるのかどうか
        if RAZPI:
            #ラズパイを用いる場合、バファサイズを指定
            caps[camera_number].set(cv.CAP_PROP_BUFFERSIZE, BUFFERSIZE)
        
        #各カメラ情報を入手
        WIDTH = caps[camera_number].get(cv.CAP_PROP_FRAME_WIDTH)
        print("カメラ番号:", camera_number, "WIDTH", WIDTH)
        HEIGHT = caps[camera_number].get(cv.CAP_PROP_FRAME_HEIGHT)
        print("カメラ番号:", camera_number, "HEIGHT", HEIGHT)
        BUFFERSIZE = caps[camera_number].get(cv.CAP_PROP_BUFFERSIZE)
        print("カメラ番号:", camera_number, "BUFFERSIZE", BUFFERSIZE)
        framerate = caps[camera_number].get(cv.CAP_PROP_FPS)
        print("カメラ番号:", camera_number, "FRAMERATE", framerate)
        

        """
        # コーデック情報を取得（未完成）
        codec_info = int(caps[camera_number].get(cv.CAP_PROP_FOURCC))
        print("codec_info:", codec_info)
        codec = chr(codec_info & 0xFF) + chr((codec_info >> 8) & 0xFF) + chr((codec_info >> 16) & 0xFF) + chr((codec_info >> 24) & 0xFF)
        print("Current codec: ", codec)
        """

        ret.append(f"ret{camera_number}")
        frame.append(f"frame{camera_number}")

        #入手したカメラ情報を、camera_info(辞書型)に格納する
        #camera_info
        # {カメラ番号: 
        # [caps   (オープンしたカメラ), 
        # retカメラ番号, 
        # frameカメラ番号, 
        # カメラのコーデック, 
        # フレームレート, 
        # WIDTH, 
        # HEIGHT, 
        # (動画撮影の場合、出力ファイル用にoutカメラ番号というものを作成(出力ファイル指定が被らないように))
        camera_info[camera_number] = []
        print(camera_info)
        camera_info[camera_number].append(caps[camera_number])
        camera_info[camera_number].append(f"ret{camera_number}")
        camera_info[camera_number].append(f"frame{camera_number}")
        camera_info[camera_number].append(camera_format)
        camera_info[camera_number].append(int(framerate))
        camera_info[camera_number].append(int(WIDTH))
        camera_info[camera_number].append(int(HEIGHT))
        if VIDEO:
            camera_info[camera_number].append(f"out{camera_number}")
        if RAZPI:
            camera_info[camera_number].append(int(BUFFERSIZE))
        #camera_info[camera_number].extend([caps[camera_number], f"ret{camera_number}", f"frame{camera_number}", camera_format, framerate, int(WIDTH), int(HEIGHT)])
        print(camera_info)
        

    return camera_info


## Usage: operate_camera()
"""
camera_numbers = {0: "camera1", 1: "camera2"}#, 3: "camera3"}
camera_format = "YUYV"
WIDTH = 1920
HEIGHT = 1080
framerate = 30
camera_info = operate_camera(camera_numbers, camera_format, WIDTH, HEIGHT, framerate)
print(camera_info)
"""



def Capture(camera_info, camera_number, save_dir, IMAGE_FORMAT, VIDEO_FORMAT, seconds=0, IMAGE=False, VIDEO=False, SHOW=True, RAZPI=False):
    print("撮影開始")
    if not camera_info[camera_number][0].isOpened():
        print("Camera is disconnected")
        sys.exit()

    WIDTH = camera_info[camera_number][5]
    HEIGHT = camera_info[camera_number][6]

    now = datetime.datetime.now()
    now_date = now.strftime("%Y_%m_%d")
    now_hour = now.strftime("%H")
    now = now.strftime("%Y_%m_%d_%H_%M_%S")

    # フォルダが存在しない場合にのみ作成
    if not os.path.exists(f"{save_dir}/{now_date}"):
        os.mkdir(f"{save_dir}/{now_date}")
        print("フォルダが作成されました。")
    else:
        print("既にフォルダが存在します。")

    # フォルダが存在しない場合にのみ作成
    if not os.path.exists(f"{save_dir}/{now_date}/{now_hour}"):
        os.mkdir(f"{save_dir}/{now_date}/{now_hour}")
        print("フォルダが作成されました。")
    else:
        print("既にフォルダが存在します。")

    camera_info[camera_number][1], camera_info[camera_number][2] = camera_info[camera_number][0].read()
    if not camera_info[camera_number][1]:
        print("Can't receive frame1 (stream end?). Exiting ...")

    if IMAGE:
        camera_info[camera_number][1], camera_info[camera_number][2] = camera_info[camera_number][0].read()
        if not camera_info[camera_number][1]:
            print("Can't receive frame1 (stream end?). Exiting ...")
        
        if len(camera_info) == 1:
            cv.imwrite(f"{save_dir}/{now_date}/{now_hour}/{now}{IMAGE_FORMAT}", camera_info[camera_number][2])
        elif len(camera_info) >= 2:
            cv.imwrite(f"{save_dir}/{now_date}/{now_hour}/{now}_{camera_number}{IMAGE_FORMAT}", camera_info[camera_number][2])


    if VIDEO:
        fourcc = cv.VideoWriter_fourcc(*camera_info[camera_number][3])
        fps = camera_info[camera_number][4]

        if len(camera_info) == 1:
            camera_info[camera_number][7] = cv.VideoWriter(f"{save_dir}/{now_date}/{now_hour}/{now}{VIDEO_FORMAT}", fourcc, fps, (int(WIDTH), int(HEIGHT)))
        elif len(camera_info) >= 2:
            camera_info[camera_number][7] = cv.VideoWriter(f"{save_dir}/{now_date}/{now_hour}/{now}_{camera_number}{VIDEO_FORMAT}", fourcc, fps, (int(WIDTH), int(HEIGHT)))

        if RAZPI:
            for i in range(camera_info[camera_number][8]):
                camera_info[camera_number][1], camera_info[camera_number][2] = camera_info[camera_number][0].read()

        for i in range(fps * seconds):
            # 1フレームずつ読み込む
            camera_info[camera_number][1], camera_info[camera_number][2] = camera_info[camera_number][0].read()
            if not camera_info[camera_number][1]:
                # フレームの読み込みに失敗した場合は終了する
                print("Can't receive frame1 (stream end?). Exiting ...")
                break

            if SHOW:
                # フレームを表示
                cv.imshow(f'camera_number: {camera_number}',camera_info[camera_number][2])
                cv.waitKey(1)
            # フレームを動画ファイルに書き込む
            camera_info[camera_number][7].write(camera_info[camera_number][2])

        # プログラムが終了する前に、動画ファイルを解放する
        camera_info[camera_number][7].release()
        # ウィンドウを閉じる
        if SHOW:
            cv.destroyWindow(f'camera_number: {camera_number}')

    print("撮影完了")

#Capture(camera_info, 1)
#Capture(caps, 1)


# 決められた時間(send_interval)後にSend関数を実行
## scheduled_time: プログラム開始時間をUNIX時間にしたもの
## send_interval: データ送信間隔
## research_place: 調査地
## Image_format: 画像ファイルの形式
## DAY, HOUR, MINUTE: データ送信間隔が、日なのか、時間なのか、分なのか
def Capture_regularly(scheduled_time, capture_interval, camera_info, camera_number, save_dir, IMAGE_FORMAT, VIDEO_FORMAT, seconds, IMAGE, VIDEO, SHOW, RAZPI, DAY=False, HOUR=False, MINUTE=False):
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enterabs(scheduled_time, 1, Capture, argument=[camera_info, camera_number, save_dir, IMAGE_FORMAT, VIDEO_FORMAT, seconds, IMAGE, VIDEO, SHOW, RAZPI])
    scheduler.run()

    if DAY:
        capture_interval = capture_interval * 86400
    elif HOUR:
        capture_interval = capture_interval * 3600
    elif MINUTE:
        capture_interval = capture_interval * 60        
    
    scheduled_time =scheduled_time + capture_interval

    

    return scheduled_time


"""
s_time = input("プログラム開始時間を入力してください")
scheduled_time = time.mktime(time.strptime(s_time, "%Y%m%d%H%M%S"))

send_interval = 1
MINUTE = True
research_place = "TEST"
framerate = 6
Image_format = ".jpg"
"""

def execution_Capture_regularly(scheduled_time, capture_interval, camera_info, camera_number, save_dir, IMAGE_FORMAT, VIDEO_FORMAT, seconds, IMAGE, VIDEO, SHOW, RAZPI, DAY, HOUR, MINUTE, SECOND):
    if IMAGE and VIDEO:
        print("Either IMAGE or VIDEO should be False.")
        sys.exit()
    if not IMAGE and not VIDEO:
        print("Either IMAGE or VIDEO should be True")
        sys.exit()
    if not IMAGE_FORMAT and not VIDEO_FORMAT:
        print("Either IMAGE_FORMAT or VIDEO_FORMAT should be set")
        sys.exit()
    if VIDEO_FORMAT and not seconds:
        print("if you want to shoot a video, seconds should be set")
        sys.exit()
    if (DAY and HOUR) or (DAY and MINUTE) or (DAY and SECOND) or (HOUR and MINUTE) or (HOUR and SECOND) or (MINUTE and SECOND):
        print("Only one of DAY, HOUR, MINUTE and SECOND should be True")
        sys.exit()
    if not (DAY or HOUR or MINUTE or SECOND):
        print("One of DAY, HOUR, MINUTE and SECOND should be True")
        sys.exit()
    if VIDEO:
        if capture_interval < seconds:
            print("capture_interval should be longer than seconds.")
    if SECOND:
        print("I guess you input SECOND")

    waiting_keyboard = True
    while waiting_keyboard:
        scheduled_time = Capture_regularly(scheduled_time, capture_interval, camera_info, camera_number, save_dir, IMAGE_FORMAT, VIDEO_FORMAT, seconds, IMAGE, VIDEO, SHOW, RAZPI, DAY, HOUR, MINUTE)
        try:
            waiting_keyboard = keyboard_wait(scheduled_time)
        except(ValueError) as e:
            print(e)
            while (scheduled_time - time.time()) < 0:
                if DAY:
                    send_interval = send_interval * 86400
                elif HOUR:
                    send_interval = send_interval * 3600
                elif MINUTE:
                    send_interval = send_interval * 60
                else:
                    print("NOT MATCH FORMAT!")
                    sys.exit()
                
                scheduled_time =scheduled_time + send_interval
            waiting_keyboard = keyboard_wait(scheduled_time)
        

        """
        wait_start_time = time.time()
        print("WE WILL WAIT 10 SECONDS. IF YOU WANT TO FINISH SENDING, YOU SHOULD PUSH q")
        while ((time.time() - wait_start_time) < 10):
            
            if keyboard.is_pressed("escape"):
                print("FINISH SENDING!!! \nGOOD JOB FOR TODAY!!!")
                break
        else:
            continue
        break
        """


"""
execution_send_regularly(scheduled_time, send_interval, research_place, framerate, Image_format, DAY, HOUR, MINUTE)
"""


"""
camera_info[camera_number][0].release()


framerate = input("framerateを入力")
print(framerate)
n_seconds = input("プログラム実行間隔を入力")
print(n_seconds)
start_time = input("プログラム開始時間を入力")

#プログラム開始時刻
dt_start = str(datetime.now().strftime("%Y%m%d%H%M%S"))
dt_start_day = datetime.now().day
dt_start_hour = datetime.now().hour
#4Ksize = 3840, 2160
WIDTH = 1920
HEIGHT = 1080
if VIDEO:
    roop = int(framerate * 10)

#撮影データ保存先
saved_dir = "../../1_data_raw/{}_{}_CaptureData/".format(dt_start, framerate)
if(os.path.isdir(saved_dir) == True):
    shutil.rmtree(saved_dir)
os.mkdir(saved_dir)
"""




"""
#camera_number = 1
save_dir = "../../1_data_raw"
IMAGE_FORMAT = ".jpg"
VIDEO_FORMAT=None
seconds = 0
IMAGE = True
VIDEO = False
SHOW = False

#Capture(camera_info, camera_number, save_dir, IMAGE_FORMAT, VIDEO_FORMAT, seconds, IMAGE)
"""


#capture_interval = int(20)

"""
execution_Capture_regularly(
    scheduled_time=scheduled_time, 
    capture_interval=int(50), 
    camera_info=camera_info, 
    save_dir="../../1_data_raw", 
    IMAGE_FORMAT=None, 
    VIDEO_FORMAT=".avi", 
    seconds=30, 
    IMAGE=False, 
    VIDEO=True, 
    SHOW=True, 
    camera_number=0, 
    DAY=False, 
    HOUR=False, 
    MINUTE=False,
    SECOND=True)

execution_Capture_regularly(
    scheduled_time=scheduled_time, 
    capture_interval=int(50), 
    camera_info=camera_info, 
    save_dir="../../1_data_raw", 
    IMAGE_FORMAT=None, 
    VIDEO_FORMAT=".avi", 
    seconds=30, 
    IMAGE=False, 
    VIDEO=True, 
    SHOW=True, 
    camera_number=1, 
    DAY=False, 
    HOUR=False, 
    MINUTE=False,
    SECOND=True)
"""


"""
camera_numbers = {0: "camera1", 1: "camera2"}#, 3: "camera3"}
camera_format = "MJPG"
WIDTH = 1920
HEIGHT = 1080
framerate = 30


camera_info = operate_camera(camera_numbers, camera_format, WIDTH, HEIGHT, framerate, VIDEO=True)
print(camera_info)

scheduled_time = input("プログラム開始時間を入力してください")
scheduled_time = time.mktime(time.strptime(scheduled_time, "%Y%m%d%H%M%S"))

executor = Executor.ThreadPoolExecutor(max_workers=2)
a = executor.submit(
    execution_Capture_regularly, 
    scheduled_time=scheduled_time, 
    capture_interval=int(40), 
    camera_info=camera_info, 
    save_dir="../../1_data_raw", 
    IMAGE_FORMAT=None, 
    VIDEO_FORMAT=".avi", 
    seconds=20, 
    IMAGE=False, 
    VIDEO=True, 
    SHOW=True, 
    camera_number=0, 
    DAY=False, 
    HOUR=False, 
    MINUTE=False,
    SECOND=True)
b = executor.submit(
    execution_Capture_regularly, 
    scheduled_time=scheduled_time, 
    capture_interval=int(40), 
    camera_info=camera_info, 
    save_dir="../../1_data_raw", 
    IMAGE_FORMAT=None, 
    VIDEO_FORMAT=".avi", 
    seconds=20, 
    IMAGE=False, 
    VIDEO=True, 
    SHOW=True, 
    camera_number=1, 
    DAY=False, 
    HOUR=False, 
    MINUTE=False,
    SECOND=True)
"""


"""
executor = Executor.ThreadPoolExecutor(max_workers=2)
a = executor.submit(execution_Capture_regularly, scheduled_time, capture_interval, camera_info, camera_number, save_dir, IMAGE_FORMAT, VIDEO_FORMAT, seconds, IMAGE, VIDEO, SHOW, DAY=False, HOUR=False, MINUTE=False)
b = executor.submit(execution_Capture_regularly, scheduled_time, capture_interval, camera_info, camera_number, save_dir, IMAGE_FORMAT, VIDEO_FORMAT, seconds, IMAGE, VIDEO, SHOW, DAY=False, HOUR=False, MINUTE=False)
"""
