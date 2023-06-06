import dropbox
import os
import shutil
import datetime
import glob
import requests
from pathlib import Path
import sched, time
import keyboard
import sys

from update_access_token import update_access_token
from get_file_creation_time import get_file_creation_time
from keyboard_wait import keyboard_wait, determine_scheduled_time
DAY = False
HOUR = False
MINUTE = False

# フォルダが存在するディレクトリのパスを取得
def scanning_folder(directory_path):
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
# Dropboxのpathは、/Kodera/{raw_or_analyzed}/{research_place}/{creation_day}/{creation_hour}/{file_name}.{file_format}"
## folder_path: アップロードしたいデータが入っているローカルのフォルダ
## file_format: アップロードしたいデータの拡張子
## dbx: dropboxのアクセストークンなどの情報. update_access_token関数で取得
## research_place: 調査地
## raw_or_analyzed: 自分は生データと解析済データでフォルダを分けているため、生データの場合は"1_data_raw", 解析済データの場合は"2_data"を入力
def Upload(folder_path, file_format, dbx, research_place, raw_or_analyzed):
    folder_paths = scanning_folder(folder_path)
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
                dropbox_path = f"/Kodera/{raw_or_analyzed}/{research_place}/{creation_day}/{creation_hour}/{file_name}.{file_format}"
                #dropboxにアップロード
                dbx.files_upload(open(file, 'rb').read(), dropbox_path)#Upload pathを設定する!
                os.remove(file)
        except(TypeError):
            pass

## Usage (Upload)
"""
folder_path = "./test"
file_format = ".txt"
dbx = update_access_token()
raw_or_analyzed = "2_data"
research_place = "TEST"
Upload(folder_path, file_format, dbx, raw_or_analyzed, research_place)
"""

# Dropboxにデータを転送するプログラム
## dbx: update_access_token関数で取得
## research_place: 調査地
## raw_data_folder: 生データのフォルダ
## file_format: 送信したいファイルの拡張子
## path_detail_list = [folder_path, file_format, research_place, raw_or_analyzed]: 送信元と送信先のパスに関する情報. ※dbxは度々更新する必要があるため、リスト型としては入れない（リストで引数として入れると変更ができない）
## path_detail_list = [
# [folder_path, file_format, dbx, research_place, raw_or_analyzed], 
# [folder_path, file_format, dbx, research_place, raw_or_analyzed], 
# [folder_path, file_format, dbx, research_place, raw_or_analyzed]
# ]
# 送信したいファイルの存在するフォルダの数だけパスを入力したリストを作成する。
# ※送信したいファイルが１つの場合、下記のようにリストの中にリストを入れる
# path_detail_list = [[information of folder path]]

def Send(path_detail_list):
    if not type(path_detail_list) == list:
        print("送信元、もしくは送信先のPATHはlist型でなければなりません")
        sys.exit()

    print("データの転送を開始します")
    
    for i in range(len(path_detail_list)):
        if not type(path_detail_list[i]) == list:
            print("送信元、もしくは送信先のPATHは\"２重の\"list型でなければなりません")
        

        Upload(path_detail_list[i][0], path_detail_list[i][1], path_detail_list[i][2], path_detail_list[i][3], path_detail_list[i][4])

    print("転送完了")




### テスト用関数
"""
def Send(research_place, dt_start, framerate, dt_day_before, dt_hour_before, Image_format):
     print("Send Function started")
"""  


# 決められた時間(send_interval)後にSend関数を実行
## scheduled_time: プログラム開始時間(%Y%m%d%H%M%S)をUNIX時間にしたもの
## send_interval: データ送信間隔
## research_place: 調査地
## Image_format: 画像ファイルの形式
## DAY, HOUR, MINUTE: データ送信間隔が、日なのか、時間なのか、分なのか
def Send_regularly(scheduled_time, send_interval, path_detail_list, DAY=False, HOUR=False, MINUTE=False, SECOND=False):
    if DAY:
        print("I guess you input DAY")
        send_interval = send_interval * 86400
    elif HOUR:
        print("I guess you input HOUR")
        send_interval = send_interval * 3600
    elif MINUTE:
        print("I guess you input MINUTE")
        send_interval = send_interval * 60
    elif SECOND:
        print("I guess you input SECOND")
        pass    
    print(send_interval)
    
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enterabs(scheduled_time, 1, Send, argument=[path_detail_list])
    scheduler.run()
    scheduled_time =scheduled_time + send_interval
    

    return scheduled_time

        #start_datetime = datetime.strptime(s_time, "%Y%m%d%H%M%S")
        #start_timestamp = datetime.timestamp(start_datetime)
        
        

        
        #scheduler.enterabs(start_timestamp, 1, Send, argument=[research_place, dt_start, framerate, dt_day_before, dt_hour_before, Image_format])
        #scheduler.run()
        
        
"""
s_time = input("プログラム開始時間を入力してください")
#scheduled_time = time.mktime(time.strptime(s_time, "%Y%m%d%H%M%S"))

send_interval = 1
MINUTE = True
research_place = "TEST"
framerate = 6
Image_format = ".jpg"
"""

def execution_send_regularly(scheduled_time, send_interval, path_detail_list, DAY, HOUR, MINUTE, SECOND):
    scheduled_time = determine_scheduled_time(scheduled_time, send_interval, DAY, HOUR, MINUTE, SECOND)

    waiting_keyboard = True
    while waiting_keyboard:
        scheduled_time = Send_regularly(scheduled_time, send_interval, path_detail_list, DAY, HOUR, MINUTE, SECOND)

        try:
            waiting_keyboard = keyboard_wait(scheduled_time)
        except(ValueError) as e:
            print(e)
            while (scheduled_time - time.time()) < 0:
                print("キーボード待機時間が不正です")
                scheduled_time = determine_scheduled_time(scheduled_time, send_interval, DAY, HOUR, MINUTE, SECOND)
            waiting_keyboard = keyboard_wait(scheduled_time)
        
        except (requests.exceptions.ConnectionError, dropbox.exceptions.AuthError, TimeoutError, requests.exceptions.ReadTimeout) as e:
            print(e)
            print("アクセストークンを更新します")
            dbx = update_access_token()
            for i in range(len(path_detail_list)):
                path_detail_list[i][2] = dbx
            
"""
scheduled_time = input("プログラム開始時間を入力してください")
scheduled_time = time.mktime(time.strptime(scheduled_time, "%Y%m%d%H%M%S"))
send_interval = 1
path_detail_list = [["../../1_data_raw", 
                     ".jpg", 
                     update_access_token(), 
                     "TEST", 
                     "1_data_raw"]]
MINUTE = True
SECOND = False
print(scheduled_time)
execution_send_regularly(scheduled_time, send_interval, path_detail_list, DAY=False, HOUR=False, MINUTE=True, SECOND=False)
"""
