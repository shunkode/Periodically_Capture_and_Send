from update_access_token import update_access_token
from Capture_and_Send import capture, send, concurrent_exucution

#設定を変更したい場合、
# Capture_data = capture()
# Send_data = send()
#の引数だけ変更する
if __name__ == "__main__":
    #画像撮影に関する設定
    Capture_data = capture( #使用するカメラの番号をリスト型で入力
                            camera_numbers = [0, 1], 
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
                            image_format = ".jpg", 
                            #動画撮影の場合の、ファイル形式を指定
                            video_format = None, 
                            #動画撮影の場合、撮影する秒数を指定
                            seconds = None, 
                            #撮影する間隔をリスト型で入力. カメラ番号と順番を対応させる．単位は後で指定可能
                            capture_interval_list = [10, 5], 
                            #画像撮影の場合、Trueに．
                            IMAGE=True, 
                            #動画撮影の場合、Trueに．
                            VIDEO=False, 
                            #プレビュー（撮影中の映像を確認）したい場合、Trueに．
                            SHOW=False, 
                            #Rasberry Piの場合、Trueに．
                            RAZPI=False, 
                            #撮影間隔の単位を指定．
                            #例：capture_interval_list=[1]
                            #    DAY=True
                            #   なら、1日ごとに撮影する
                            DAY=False, 
                            HOUR=False, 
                            MINUTE=False, 
                            SECOND=True
                            )
    
    dbx = update_access_token() #変更しない
    Send_data = send(   #送信したいデータの存在するフォルダの数だけリストを作成
                        #path_detail_listの情報: [ローカルのフォルダパス, 送信したいファイル形式, 送信したいDropboxのフォルダのパス]
                        #例（送信したいフォルダ数が1つの場合）
                        #path_detail_list=[["local_folder_path", file_format, dbx, dropbox_folder_path]]
                        #例（送信したいフォルダ数が2つの場合）
                        #path_detail_list=[["local_folder_path", file_format, dbx, dropbox_folder_path], 
                        #                   ["local_folder_path", file_format, dbx, dropbox_folder_path]]
                        path_detail_list=[["../../1_data_raw", 
                       ".jpg", 
                        dbx, #変更しない
                       "Kodera/1_data_raw/TEST"
                       ]],
                        #データ送信間隔
                        send_interval=3, 
                        #データ送信間隔の単位
                        DAY=False, 
                        HOUR=False, 
                        MINUTE=True, 
                        SECOND=False
                    )

    concurrent_exucution(Capture_data, Send_data)

    #撮影終了後、もう一度転送する
    Send_data.Send()

 