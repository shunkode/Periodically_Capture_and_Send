from update_access_token import update_access_token
from Capture_and_Send import capture, send, concurrent_exucution
import multiprocessing

#設定を変更したい場合、
# Capture_data = capture()
# Send_data = send()
#の引数だけ変更する

time_Queue = multiprocessing.Queue()
frame_Queue = multiprocessing.Queue()

if __name__ == "__main__":
    #画像撮影に関する設定
    Capture_data = capture( #使用するカメラの番号をリスト型で入力
                            camera_numbers = [1], 
                            #使用するカメラのコーデックを指定
                            camera_format = "MJPG", 
                            #解像度を指定
                            width = int(1920), 
                            height = int(1080), 
                            #フレームレートを指定
                            framerate = int(30), 
                            #Rasberry Piを使用する場合、バッファサイズを指定
                            buffersize = 4, 
                            #保存するローカルのディレクトリパスを指定
                            save_dir = "../../1_data_raw", 
                            #画像撮影の場合の、ファイル形式を指定
                            image_format = None, 
                            #動画撮影の場合の、ファイル形式を指定
                            video_format = ".avi", 
                            #動画撮影の場合、撮影する秒数を指定
                            seconds = 10, 
                            #撮影する間隔をリスト型で入力. カメラ番号と順番を対応させる．単位は後で指定可能
                            capture_interval_list = [30], 
                            capture_time_Queue=time_Queue, 
                            frame_Queue=frame_Queue, 
                            #画像撮影の場合、Trueに．
                            IMAGE=False, 
                            #動画撮影の場合、Trueに．
                            VIDEO=True, 
                            #プレビュー（撮影中の映像を確認）したい場合、Trueに．
                            SHOW=True, 
                            #Rasberry Piの場合、Trueに．
                            RAZPI=False, 
                            #撮影間隔の単位を指定．
                            #例：capture_interval_list=[1]
                            #    DAY=True
                            #   なら、1日ごとに撮影する
                            DAY=False, 
                            HOUR=False, 
                            MINUTE=False, 
                            SECOND=True, 
                            #PICAMERA=True
                            )
    
    Send_data = None
    """
    dbx = update_access_token() #変更しない
    Send_data = send(   #送信したいデータの存在するフォルダの数だけリストを作成
                        #path_detail_listの情報: [ローカルのフォルダパス, 送信したいファイル形式, 送信したいDropboxのフォルダのパス]
                        #例（送信したいフォルダ数が1つの場合）
                        #path_detail_list=[["local_folder_path", file_format, dbx, dropbox_folder_path]]
                        #例（送信したいフォルダ数が2つの場合）
                        #path_detail_list=[["local_folder_path", file_format, dbx, dropbox_folder_path], 
                        #                   ["local_folder_path", file_format, dbx, dropbox_folder_path]]
                        path_detail_list=[["../../1_data_raw", 
                       ".avi", 
                        dbx, #変更しない
                       "Kodera/1_data_raw/TEST"
                       ]],
                        #データ送信間隔
                        send_interval=1, 
                        #データ送信間隔の単位
                        DAY=False, 
                        HOUR=False, 
                        MINUTE=True, 
                        SECOND=False
                    )
    """


        


    """
    
    """

    
    concurrent_exucution(Capture_data, Send_data, interruption_time="03:00", restart_time="10:00")

    #撮影終了後、もう一度転送する
    if Send_data:
        Send_data.Send()
    elif not Send_data:
        print("最後のデータ転送も行いません。")

 
