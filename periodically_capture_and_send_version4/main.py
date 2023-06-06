# ライブラリをインポート
import concurrent.futures as Executor
import time
import platform


from Send import Upload, Send, Send_regularly, execution_send_regularly
from update_access_token import update_access_token
from capture import operate_camera, execution_Capture_regularly



if __name__ == "__main__":
    # camera番号を指定
    camera_numbers = {0: "camera1"}#, 1: "camera2"}#, 3: "camera3"}
    # カメラのコーデックを指定
    camera_format = "MJPG"
    # 解像度を指定
    WIDTH = 1920
    HEIGHT = 1080
    # フレームレートを指定
    framerate = 30

   
    # path_detail_list = ["送信元のフォルダ名", 
    #                   "送信したいファイル形式", 
    #                   "Dropboxのアクセストークン", 
    #                   "調査地"
    #                   "データ区分"
    #                   ]
    path_detail_list = [["../../1_data_raw", ".jpg", update_access_token(), "TEST", "1_data_raw"]]
    
    # カメラを起動して、情報を取得する
    ## camera_numbers: カメラの番号（前に入力済）
    ## camera_format: カメラのコーデック（前に入力済）
    ## WIDTH, HEIGHT: 解像度（前に入力済）
    ## framerate: フレームレート（前に入力済）
    ## VIDEO: 動画撮影の場合、Trueにする
    ## RAZPI: ラズパイ使用の場合、Trueにする
    camera_info = operate_camera(camera_numbers, camera_format, WIDTH, HEIGHT, framerate, VIDEO=True, RAZPI=True)
    print(camera_info)

    
    # プログラム開始時間を入力してくださいと出力される
    ## 年月日時間分秒で入力: example. 20230428142300（←2023/4/28 14:23:00）                    
    scheduled_time = input("プログラム開始時間を入力してください")
    # UNIX時間（積算秒数）に直す
    scheduled_time = time.mktime(time.strptime(scheduled_time, "%Y%m%d%H%M%S"))
    
    """
    execution_Capture_regularly(
        scheduled_time=scheduled_time, 
        capture_interval=int(15), 
        camera_info=camera_info, 
        save_dir="../..//1_data_raw", 
        IMAGE_FORMAT=".jpg", 
        VIDEO_FORMAT=None, 
        seconds=None,
        IMAGE=True,  
        VIDEO=False, 
        SHOW=False,
        RAZPI=False, 
        camera_number=1, 
        DAY=False, 
        HOUR=False, 
        MINUTE=False,
        SECOND=True)
    
    """
    # 複数の作業を同時進行する(max_workers: 最大作業数)
    executor = Executor.ThreadPoolExecutor(max_workers=3)
    # execution_Capture_regularly(
    ## scheduled_time: 開始時間（前に入力済み）
    ## capture_interval: 撮影間隔（ここは新たに入力）
    ## camera_info: カメラの情報（前に入力済み）
    ## save_dir: 撮影データを入れるフォルダのパスを入力（ここは新たに入力）
    ## IMAGE_FORMAT, VIDEO_FORMAT: 拡張子を設定（ここは新たに入力）
    ## seconds: 動画撮影の場合、撮影する秒数を入力（ここは新たに入力）
    ## IMAGE, VIDEO: IMAGEがTrueなら、画像で撮影、
    ##               VIDEOがTrueなら動画で撮影（ここは新たに入力）
    ## SHOW: Trueなら、今撮影してるものをプレビューする
    ## camera_number: 扱いたいカメラの番号を設定（ここは新たに入力）
    ## DAY, HOUR, MINUTE, SECOND: intervalの単位。
    ##                 example: seconds=2, HOUR=Trueなら、２時間ごとに撮影
    # ）
    
    a = executor.submit(
        execution_Capture_regularly, 
        scheduled_time=scheduled_time, 
        capture_interval=int(20)
        , #ここ変更
        camera_info=camera_info, 
        save_dir="../../1_data_raw", #ここ変更
        IMAGE_FORMAT=".jpg", #ここ変更
        VIDEO_FORMAT=None, #ここ変更
        seconds=None, #ここ変更
        IMAGE=True,  #ここ変更
        VIDEO=False, #ここ変更
        SHOW=False, #ここ変更
        RAZPI=False, 
        camera_number=0, #ここ変更
        DAY=False, #ここ変更
        HOUR=False, #ここ変更
        MINUTE=False,#ここ変更
        SECOND=True)#ここ変更
    
    
    # 2台以上扱いたい場合、
    # camera_numberを変えて同じ関数を実行
    b = executor.submit(
        execution_Capture_regularly, 
        scheduled_time=scheduled_time, 
        capture_interval=int(15), 
        camera_info=camera_info, 
        save_dir="../../1_data_raw", 
        IMAGE_FORMAT=".jpg", 
        VIDEO_FORMAT=None, 
        seconds=None, 
        IMAGE=True, 
        VIDEO=False, 
        SHOW=False, 
        RAZPI=False, 
        camera_number=1, 
        DAY=False, 
        HOUR=False, 
        MINUTE=False,
        SECOND=True)
    
    # Dropboxにデータ転送
    # execution_send_regularly(
    # scheduled_time: 開始時間を入力（前に入力済）
    # send_interval: 送信する間隔を入力（ここは新たに入力）
    # path_detail_list: 送信元と送信先のパス、アクセストークンを入力（前に入力済）
    ## DAY, HOUR, MINUTE, SECOND: intervalの単位。
    ##                 example: seconds=2, HOUR=Trueなら、２時間ごとに撮影
    # ）
    # )
    c = executor.submit(
        execution_send_regularly, 
        scheduled_time=scheduled_time, 
        send_interval=1, #ここ変更
        path_detail_list= path_detail_list, 
        DAY=False, #ここ変更
        HOUR=False, #ここ変更
        MINUTE=True, #ここ変更
        SECOND=False) #ここ変更
    
    # 全てのタスクが完了するまで待つ()
    executor.shutdown()
    
    print("LAST SENDING WILL START")

    # 最後にもう一度データ転送する
    Send(path_detail_list)
    
    
