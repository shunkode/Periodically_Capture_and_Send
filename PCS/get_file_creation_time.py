import os.path
import platform
import time
import dropbox

def get_folder_name(directory):
    # ディレクトリ内のフォルダ名を取得
    folder_names = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    print(folder_names)
    """
    # 取得したフォルダ名を表示
    for folder_name in folder_names:
        print(folder_name)
        folder_name_list.append(folder_name)
    """
    return folder_names
    

def get_file_creation_time(file_path):
    """
    ファイルの作成時刻をUNIX時間で返す
    取得できない場合は最終更新時刻を返す
    """
    if not os.path.exists(file_path):
        return None
    
    system = platform.system()
    if system == 'Windows':
        return os.path.getctime(file_path)
    elif system == 'Darwin' or system == 'Linux':
        print(f"system: {system}")
        stat = os.stat(file_path)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime
    else:
        raise ValueError("サポートされていないOSです。")


# dropboxにフォルダーを作成する
## raw_or_analyzed: 1_data_raw or 2_data
def create_dropbox_folder(file_path, dbx, raw_or_analyzed, research_place):
    # get_file_creation_timeによりファイルの作成時間を表示
    creation_time = get_file_creation_time(file_path)
    # get_file_creation_timeにより得られたファイルの作成日を取得
    creation_day = time.strftime("%Y_%m_%d", time.localtime(creation_time))
    # get_file_creation_hourにより得られたファイルの作成時刻
    creation_hour = time.strftime("%H", time.localtime(creation_time))

    dropbox_path = f"/Kodera/{raw_or_analyzed}/{research_place}/{creation_day}/{creation_hour}"
    try:
        dbx.files_create_folder(dropbox_path)
    except dropbox.exceptions.ApiError as e:
        print(e, "作成しようとしたフォルダーは既に存在している可能性があります。")
        pass

"""
import update_access_token
dbx = update_access_token.update_access_token()
dbx.files_upload(open("test.txt", 'rb').read(),
                  "/Kodera/2_data/Watarase_River/2023_04_04/17/test/test.txt")  
"""
                  
## Usage (get_file_creation_time)
"""
file_path = "test.txt"
creation_time = get_file_creation_time(file_path)
print("ファイルの作成時刻：", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time)))
print("ファイルの作成日：", time.strftime('%Y/%m/%d', time.localtime(creation_time)))
print("ファイルの作成時刻：", time.strftime('%H:%M:%S', time.localtime(creation_time)))
"""

##Usage (create_dropbox_folder)
"""
import update_access_token
dbx = update_access_token.update_access_token()
file_path = "test.txt"
create_dropbox_folder(file_path, dbx, "2_data", "Watarase_River")
print("Succeeded")
"""


### 没プログラム
"""
def check_folder_exists(path):
    ""
    Dropbox上に指定されたパスのフォルダが存在するかどうかを判定する関数

    Parameters:
    path (str): Dropbox上のパス

    Returns:
    bool: フォルダが存在する場合はTrue、存在しない場合はFalse
    ""
    # Dropbox APIを使用するためのアクセストークン
    # アクセストークン

    # Dropbox APIのクライアントオブジェクトを作成
    try:
        # アクセストークン
        dbx = update_access_token()
    except AuthError as e:
        print('認証エラーが発生しました：', e)
        return False

    # 指定されたパスのフォルダが存在するかどうかを判定
    try:
        metadata = dbx.files_get_metadata(path)
        if isinstance(metadata, dropbox.files.FolderMetadata):
            print('フォルダが存在します。')
            return True
        else:
            print('指定されたパスはフォルダではありません。')
            return False
    
    except ApiError as e:
        print("e.error: ", e.error)
        print("get_path: ", e.error.get_path())
        print(dir(e.error.get_path()))
        
        if e.error.is_path() and e.error.get_path().is_conflict():
            print('指定されたパスには複数のファイル/フォルダが存在します。')
            return False
        print("type: ", type("LookupError('not_fouond', None)"))
        print(str(e.error.get_path())) == "LookupError('not_fouond', None)"
        if e.error.is_path() and e.error.get_path() == LookupError:#not e.error.get_path().is_conflict():
            try:
                print("pathは正常です")
            except(e.error.get_path() == LookupError('not_found', None)):
                print('指定されたパスにフォルダは存在しません。')
            return False
        else:
            print('エラーが発生しました：', e)
            return False
    


check_folder_exists("/Kodera/2_data/Watarase_River/WataraseRiver_20230207000600_30.0/08_30.0")
"""

"""
def confirm_Dropbox_folder(dbx_folder_path):
    # アクセストークン
    dbx = update_access_token()

    try:
        # フォルダのメタデータを取得
        metadata = dbx.files_get_metadata(dbx_folder_path)

        # フォルダが存在するかどうかを判定
        if isinstance(metadata, dropbox.files.FolderMetadata):
            print('フォルダが存在します')
        else:
            print('フォルダではありません')

    except AuthError as e:
        print('認証エラーが発生しました：', e)
    except ApiError as e:
        if e.error.is_path(): #and \
                print("ABCDE")
        elif e.error.get_path().is_conflict() and \
             e.error.get_path().get_conflict().is_folder():
                print('フォルダが存在しません')
        else:
            print('APIエラーが発生しました：', e)

confirm_Dropbox_folder("/Kodera/2_data/Watarase_River/WataraseRiver_20230207000600_30.0/08_30.0")
"""
