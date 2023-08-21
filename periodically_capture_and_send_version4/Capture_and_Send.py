import sched, time
import numpy as np
import cv2 as cv
import os
import datetime
import concurrent.futures as Executor 
import sys
import dropbox
import glob
import requests
from pathlib import Path

from update_access_token import update_access_token
from get_file_creation_time import get_file_creation_time
from keyboard_wait import keyboard_wait, determine_scheduled_time

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
#camera_numbers, camera_format, WIDTH, HEIGHT, framerate, VIDEO=False, BUFFERSIZE=4, RAZPI=False

class capture:

    def __init__(self, 
                 camera_numbers, 
                 camera_format, 
                 width, 
                 height, 
                 framerate, 
                 buffersize,
                 save_dir, 
                 image_format, 
                 video_format, 
                 seconds, 
                 capture_interval_list, 
                 IMAGE=True, 
                 VIDEO=False, 
                 SHOW=False, 
                 RAZPI=False, 
                 DAY=False, 
                 HOUR=False, 
                 MINUTE=False, 
                 SECOND=True):
        self.camera_numbers = camera_numbers
        self.camera_format = camera_format
        self.width = width
        self.height = height
        self.framerate = framerate
        self.buffersize = buffersize
        self.RAZPI = RAZPI
        self.save_dir = save_dir
        self.image_format = image_format
        self.video_format = video_format 
        self.seconds = seconds 
        self.IMAGE = IMAGE 
        self.VIDEO = VIDEO
        self.SHOW = SHOW 
        self.RAZPI = RAZPI 
        self.DAY = DAY 
        self.HOUR = HOUR
        self.MINUTE = MINUTE 
        self.SECOND = SECOND


        caps = {}
        camera_info = {}
        #カメラ番号ごとに以下の操作を実施
        for index, camera_number in enumerate(self.camera_numbers):
            print("index: ", index)
            #カメラを起動
            caps[camera_number] = cv.VideoCapture(camera_number)
            #起動できなければ抜ける
            if not caps[camera_number].isOpened():
                print(f"Cannot open camera{camera_number}")
                sys.exit()
            #カメラのコーデックを指定
            caps[camera_number].set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*self.camera_format))#"Y", "U", "Y", "V""M", "J", "P", "G"
            #カメラの解像度(WIDTH)を指定
            caps[camera_number].set(cv.CAP_PROP_FRAME_WIDTH, self.width)
            #カメラの解像度(HEIGHT)を指定
            caps[camera_number].set(cv.CAP_PROP_FRAME_HEIGHT, self.width)
            #カメラのフレームレートを指定
            caps[camera_number].set(cv.CAP_PROP_FPS, self.framerate)
            #ラズパイを用いて動作させるのかどうか
            if self.RAZPI:
                #ラズパイを用いる場合、バファサイズを指定
                caps[camera_number].set(cv.CAP_PROP_BUFFERSIZE, self.buffersize)
            
            #各カメラ情報を入手
            width = caps[camera_number].get(cv.CAP_PROP_FRAME_WIDTH)
            print("カメラ番号:", camera_number, "WIDTH", width)
            height = caps[camera_number].get(cv.CAP_PROP_FRAME_HEIGHT)
            print("カメラ番号:", camera_number, "HEIGHT", height)
            if self.RAZPI:
                buffersize = caps[camera_number].get(cv.CAP_PROP_BUFFERSIZE)
                print("カメラ番号:", camera_number, "BUFFERSIZE", buffersize)
            framerate = caps[camera_number].get(cv.CAP_PROP_FPS)
            print("カメラ番号:", camera_number, "FRAMERATE", framerate)
            

            """
            # コーデック情報を取得（未完成）
            codec_info = int(caps[camera_number].get(cv.CAP_PROP_FOURCC))
            print("codec_info:", codec_info)
            codec = chr(codec_info & 0xFF) + chr((codec_info >> 8) & 0xFF) + chr((codec_info >> 16) & 0xFF) + chr((codec_info >> 24) & 0xFF)
            print("Current codec: ", codec)
            """


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
            camera_info[camera_number].append(int(width))
            camera_info[camera_number].append(int(height))
            camera_info[camera_number].append(capture_interval_list[index])
            if VIDEO:
                camera_info[camera_number].append(f"out{camera_number}")
            if RAZPI:
                camera_info[camera_number].append(int(buffersize))
            #camera_info[camera_number].extend([caps[camera_number], f"ret{camera_number}", f"frame{camera_number}", camera_format, framerate, int(WIDTH), int(HEIGHT)])
            print(camera_info)
            
        self.camera_info = camera_info

    


    def Capture(self, camera_number):
        print("撮影開始")
        if not self.camera_info[camera_number][0].isOpened():
            print("Camera is disconnected")
            sys.exit()

        WIDTH = self.camera_info[camera_number][5]
        HEIGHT = self.camera_info[camera_number][6]

        now = datetime.datetime.now()
        now_date = now.strftime("%Y_%m_%d")
        now_hour = now.strftime("%H")
        now = now.strftime("%Y_%m_%d_%H_%M_%S")

        # フォルダが存在しない場合にのみ作成
        if not os.path.exists(f"{self.save_dir}/{now_date}"):
            os.mkdir(f"{self.save_dir}/{now_date}")
            print("フォルダが作成されました。")
        else:
            print("既にフォルダが存在します。")

        # フォルダが存在しない場合にのみ作成
        if not os.path.exists(f"{self.save_dir}/{now_date}/{now_hour}"):
            os.mkdir(f"{self.save_dir}/{now_date}/{now_hour}")
            print("フォルダが作成されました。")
        else:
            print("既にフォルダが存在します。")

        self.camera_info[camera_number][1], self.camera_info[camera_number][2] = self.camera_info[camera_number][0].read()
        if not self.camera_info[camera_number][1]:
            print("Can't receive frame1 (stream end?). Exiting ...")

        if self.IMAGE:
            self.camera_info[camera_number][1], self.camera_info[camera_number][2] = self.camera_info[camera_number][0].read()
            if not self.camera_info[camera_number][1]:
                print("Can't receive frame1 (stream end?). Exiting ...")
            
            if len(self.camera_info) == 1:
                cv.imwrite(f"{self.save_dir}/{now_date}/{now_hour}/{now}{self.image_format}", self.camera_info[camera_number][2])
            elif len(self.camera_info) >= 2:
                cv.imwrite(f"{self.save_dir}/{now_date}/{now_hour}/{now}_{camera_number}{self.image_format}", self.camera_info[camera_number][2])

        if self.VIDEO:
            fourcc = cv.VideoWriter_fourcc(*self.camera_info[camera_number][3])
            fps = self.camera_info[camera_number][4]

            if len(self.camera_info) == 1:
                self.camera_info[camera_number][8] = cv.VideoWriter(f"{self.save_dir}/{now_date}/{now_hour}/{now}{self.video_format}", fourcc, fps, (int(WIDTH), int(HEIGHT)))
            elif len(self.camera_info) >= 2:
                self.camera_info[camera_number][8] = cv.VideoWriter(f"{self.save_dir}/{now_date}/{now_hour}/{now}_{camera_number}{self.video_format}", fourcc, fps, (int(WIDTH), int(HEIGHT)))

            if self.RAZPI:
                for i in range(self.camera_info[camera_number][9]):
                    self.camera_info[camera_number][1], self.camera_info[camera_number][2] = self.camera_info[camera_number][0].read()

            for i in range(fps * self.seconds):
                # 1フレームずつ読み込む
                self.camera_info[camera_number][1], self.camera_info[camera_number][2] = self.camera_info[camera_number][0].read()
                if not self.camera_info[camera_number][1]:
                    # フレームの読み込みに失敗した場合は終了する
                    print("Can't receive frame1 (stream end?). Exiting ...")
                    break

                if self.SHOW:
                    # フレームを表示
                    cv.imshow(f'camera_number: {camera_number}',self.camera_info[camera_number][2])
                    cv.waitKey(1)
                # フレームを動画ファイルに書き込む
                self.camera_info[camera_number][8].write(self.camera_info[camera_number][2])

            # プログラムが終了する前に、動画ファイルを解放する
            self.camera_info[camera_number][8].release()
            # ウィンドウを閉じる
            if self.SHOW:
                cv.destroyWindow(f'camera_number: {camera_number}')

        print("撮影完了")



    def Capture_regularly(self, scheduled_time, camera_number):
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enterabs(scheduled_time, 1, self.Capture, argument=[camera_number])
        scheduler.run()

        
        if self.DAY:
            scheduled_time =scheduled_time + self.camera_info[camera_number][7]  * 86400
        elif self.HOUR:
            scheduled_time =scheduled_time + self.camera_info[camera_number][7]  * 3600
        elif self.MINUTE:
            scheduled_time =scheduled_time + self.camera_info[camera_number][7]  * 60
        elif self.SECOND:
            scheduled_time =scheduled_time + self.camera_info[camera_number][7]   
        else:
            print("Capture: Not match interval format.") 

        return scheduled_time
    

    def execution_Capture_regularly(self, scheduled_time, camera_number):
        if self.IMAGE and self.VIDEO:
            print("Either IMAGE or VIDEO should be False.")
            sys.exit()
        if not self.IMAGE and not self.VIDEO:
            print("Either IMAGE or VIDEO should be True")
            sys.exit()
        if not self.image_format and not self.video_format:
            print("Either IMAGE_FORMAT or VIDEO_FORMAT should be set")
            sys.exit()
        if self.video_format and not self.seconds:
            print("if you want to shoot a video, seconds should be set")
            sys.exit()
        if (self.DAY and self.HOUR) or (self.DAY and self.MINUTE) or (self.DAY and self.SECOND) or (self.HOUR and self.MINUTE) or (self.HOUR and self.SECOND) or (self.MINUTE and self.SECOND):
            print("Only one of DAY, HOUR, MINUTE and SECOND should be True")
            sys.exit()
        if not (self.DAY or self.HOUR or self.MINUTE or self.SECOND):
            print("One of DAY, HOUR, MINUTE and SECOND should be True")
            sys.exit()
        if self.VIDEO:
            # 撮影間隔(capture_interval) < 撮影時間(seconds)なら終了
            if self.camera_info[camera_number][7] < self.seconds:
                print("capture_interval should be longer than seconds.")
        if self.SECOND:
            print("I guess you input SECOND")
            

        #scheduled_time = input("プログラム開始時間を入力してください")
        # UNIX時間（積算秒数）に直す
        #scheduled_time = time.mktime(time.strptime(scheduled_time, "%Y%m%d%H%M%S"))

        waiting_keyboard = True
        while waiting_keyboard:
            scheduled_time = self.Capture_regularly(scheduled_time, camera_number)
            try:
                waiting_keyboard = keyboard_wait(scheduled_time)
            except(ValueError) as e:
                print(e)
                while (scheduled_time - time.time()) < 0:
                    print("Capture: キーボード待機時間が負です.")
                    scheduled_time = determine_scheduled_time(scheduled_time, self.camera_info[camera_number][7], self.DAY, self.HOUR, self.MINUTE, self.SECOND)
                    
                waiting_keyboard = keyboard_wait(scheduled_time)




    """
    def concurrent_execution(self):
        for camera_dict in self.camera_info:
            executor = Executor.ThreadPoolExecutor(max_workers=3)

            a = executor.submit(
                self.execution_Capture_regularly, 
                self
                camera_number
            )
    """

"""
## Usage
test = capture(camera_numbers = [1], 
                camera_format = "MJPG", 
                width = int(1920), 
                height = int(1080), 
                framerate = int(30), 
                buffersize = 4, 
                save_dir = "../../1_data_raw", 
                image_format = ".jpg", 
                video_format = None, 
                seconds = None, 
                capture_interval_list = [10], 
                IMAGE=True, 
                VIDEO=False, 
                SHOW=False, 
                RAZPI=False, 
                DAY=False, 
                HOUR=False, 
                MINUTE=False, 
                SECOND=True
                )

test.execution_Capture_regularly(1)
"""



class send:
    def __init__(self, 
                 path_detail_list,
                 send_interval, 
                 DAY, 
                 HOUR, 
                 MINUTE, 
                 SECOND):
        self.path_detail_list = path_detail_list
        self.send_interval = send_interval
        self.DAY = DAY
        self.HOUR = HOUR
        self.MINUTE = MINUTE
        self.SECOND = SECOND

    # フォルダが存在するディレクトリのパスを取得
    def scanning_folder(self, directory_path):
        # ディレクトリ以下に存在するフォルダのパスを再帰的に取得
        directory_path_list = []
        for curDir, dirs, files in os.walk(directory_path):
            print('===================')
            print("現在のディレクトリ: " , curDir)
            print("内包するディレクトリ:" , dirs)
            print("内包するファイル: " , files)

            if (len(dirs) == 0) and (len(files) == 0):
                curDir = curDir.replace("\\", "/")
                if curDir == directory_path:
                    continue
                print("delete: ", curDir)
                os.rmdir(curDir)
                
            elif len(files) >= 1:
                curDir = curDir.replace("\\", "/")
                #print(curDir)
                directory_path_list.append(curDir)
        return directory_path_list


    # {folder_path}内の拡張子が{file_format}のものをDropboxにアップロードする関数
    # Dropboxの保存したいフォルダー内に、作成日/作成時間
    ## folder_path: アップロードしたいデータが入っているローカルのフォルダ
    ## file_format: アップロードしたいデータの拡張子
    ## dbx: dropboxのアクセストークンなどの情報. update_access_token関数で取得
    ## dbx_folder_path: 保存したいDropboxフォルダーのパス(ex. Kodera/{raw_or_analyzed}/{research_place})


    ## research_place: 調査地
    ## raw_or_analyzed: 自分は生データと解析済データでフォルダを分けているため、生データの場合は"1_data_raw", 解析済データの場合は"2_data"を入力
    def Upload(self, folder_path, file_format, dbx, dbx_folder_path):
        folder_paths = self.scanning_folder(folder_path)
        for folder_path in folder_paths:
            # {folder_path}内の拡張子{file_format}のもののpathを全て取得
            files = glob.glob(f"{folder_path}/*{file_format}")
            # 取得したpathの1つ1つに対して次の操作を実行する
            try:
                for file in files:
                    # ファイルの作成時間を取得
                    creation_time = get_file_creation_time(file)
                    # ファイルの作成日を取得
                    creation_day = time.strftime("%Y_%m_%d", time.localtime(creation_time))
                    # ファイルの作成時刻を取得
                    creation_hour = time.strftime("%H", time.localtime(creation_time))
                    # ファイル名を取得
                    file_name = Path(file).stem
                    #dropboxのpathを設定
                    dropbox_path = f"/{dbx_folder_path}/{creation_day}/{creation_hour}/{file_name}.{file_format}"
                    #dropboxにアップロード
                    dbx.files_upload(open(file, 'rb').read(), dropbox_path)#Upload pathを設定する!
                    os.remove(file)
            except(TypeError) as e:
                print(e)
                pass

    # Dropboxにデータを転送するプログラム
    ## dbx: update_access_token関数で取得
    ## research_place: 調査地
    ## raw_data_folder: 生データのフォルダ
    ## file_format: 送信したいファイルの拡張子
    ## path_detail_list = [[folder_path, file_format, dbx_folder_path, send_interval]]: 送信元と送信先のパスに関する情報.必ず"2重の"リストにする
    ## path_detail_list = [
    # [folder_path, file_format, dbx, dbx_folder_path], 
    # [folder_path, file_format, dbx, dbx_folder_path], 
    # [folder_path, file_format, dbx, dbx_folder_path]
    # ]
    # 送信したいファイルの存在するフォルダの数だけパスを入力したリストを作成する。
    # ※送信したいファイルが１つの場合、下記のようにリストの中にリストを入れる
    # path_detail_list = [[information of folder path]]

    def Send(self):
        if not type(self.path_detail_list) == list:
            print("送信元、もしくは送信先のPATHはlist型でなければなりません")
            sys.exit()

        print("データの転送を開始します")
        
        for i in range(len(self.path_detail_list)):
            if not type(self.path_detail_list[i]) == list:
                print("送信元、もしくは送信先のPATHは\"２重の\"list型でなければなりません")      

            self.Upload(self.path_detail_list[i][0], self.path_detail_list[i][1], self.path_detail_list[i][2], self.path_detail_list[i][3])

        print("転送完了")


    # 決められた時間(send_interval)後にSend関数を実行
    ## scheduled_time: プログラム開始時間(%Y%m%d%H%M%S)をUNIX時間にしたもの
    ## send_interval: データ送信間隔
    ## research_place: 調査地
    ## Image_format: 画像ファイルの形式
    ## DAY, HOUR, MINUTE, SECOND: データ送信間隔の単位（日、時、分、秒）
    def Send_regularly(self, scheduled_time):

        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enterabs(scheduled_time, 1, self.Send, argument=[])
        scheduler.run()

        if self.DAY:
            print("I guess you input DAY")
            scheduled_time =scheduled_time + self.send_interval * 86400
        elif self.HOUR:
            print("I guess you input HOUR")
            scheduled_time =scheduled_time + self.send_interval * 3600
        elif self.MINUTE:
            print("I guess you input MINUTE")
            scheduled_time =scheduled_time + self.send_interval * 60
        elif self.SECOND:
            scheduled_time =scheduled_time + self.send_interval
            print("I guess you input SECOND")
            pass    
        print(self.send_interval)
        
        
        #scheduler = sched.scheduler(time.time, time.sleep)
        #scheduler.enterabs(scheduled_time, 1, self.Send, argument=[])
        #scheduler.run()
        #scheduled_time =scheduled_time + self.send_interval
        

        return scheduled_time

    def execution_send_regularly(self, scheduled_time):
        scheduled_time = determine_scheduled_time(scheduled_time, self.send_interval, self.DAY, self.HOUR, self.MINUTE, self.SECOND)

        waiting_keyboard = True
        while waiting_keyboard:
            scheduled_time = self.Send_regularly(scheduled_time)

            try:
                waiting_keyboard = keyboard_wait(scheduled_time)
            except(ValueError) as e:
                print(e)
                while (scheduled_time - time.time()) < 0:
                    print("Send: キーボード待機時間が負です.")
                    scheduled_time = determine_scheduled_time(scheduled_time, self.send_interval, self.DAY, self.HOUR, self.MINUTE, self.SECOND)
                waiting_keyboard = keyboard_wait(scheduled_time)
            
            except (requests.exceptions.ConnectionError, dropbox.exceptions.AuthError, TimeoutError, requests.exceptions.ReadTimeout) as e:
                print(e)
                print("アクセストークンを更新します")
                dbx = update_access_token()
                for i in range(len(self.path_detail_list)):
                    self.path_detail_list[i][2] = dbx
                

import concurrent.futures
def concurrent_exucution(Capture, Send):
    camera_info = Capture.camera_info

    scheduled_time = input("プログラム開始時間を入力してください")
    # UNIX時間（積算秒数）に直す
    scheduled_time = time.mktime(time.strptime(scheduled_time, "%Y%m%d%H%M%S"))
    
    camera_numbers_list = list(camera_info)
    print(camera_numbers_list)

    # CPUのコア数を調べる
    num_cores = os.cpu_count()
    if ((len(camera_numbers_list) + 2) > num_cores):
        print("WARNING: 要求される作業量にCPUのコア数が対応できない可能性があります")

    # Executor.ThreadPoolExecutorの実行用に、関数と引数のリストを作成する
    executor_func_list = []
    executor_args_list = []
    # 撮影用の関数, 引数リスト
    for camera_number in camera_numbers_list:
        executor_func_list.append(Capture.execution_Capture_regularly)
        executor_args_list.append([scheduled_time, camera_number])
    # データ送信用の関数、引数リスト
    executor_func_list.append(Send.execution_send_regularly)
    executor_args_list.append([scheduled_time])

    # Create a ThreadPoolExecutor with max_workers
    max_workers = len(camera_numbers_list) + 1  # Adjust the number of workers as needed
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Use zip to pair each task with its corresponding argument pair and submit to executor
            futures = [executor.submit(func, *args) for func, args in zip(executor_func_list, executor_args_list)]

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)
            
    # Check if any errors occurred and print exception information
    for future in futures:
        try:
            # Accessing the result will raise an exception if the task had an error
            result = future.result()
            print("result: ", result)
        except Exception as e:
            print(f"Error occurred: {e}")

    """
    def concurrent_execution(self):
        for camera_dict in self.camera_info:
            executor = Executor.ThreadPoolExecutor(max_workers=3)

            a = executor.submit(
                self.execution_Capture_regularly, 
                self
                camera_number
            )
    """


"""
test = Send(path_detail_list=[["../../1_data_raw", 
                       ".jpg", 
                       update_access_token(), 
                       "Kodera/1_data_raw/TEST"
                       ]],
     send_interval=1, 
     DAY=False, 
     HOUR=False, 
     MINUTE=False, 
     SECOND=True
)
scheduled_time = input("プログラム開始時間を入力してください")
# UNIX時間（積算秒数）に直す
scheduled_time = time.mktime(time.strptime(scheduled_time, "%Y%m%d%H%M%S"))
test.execution_send_regularly(scheduled_time)
"""





