#解析するデータが画像か動画か、判定するプログラム

import sys

def confirm_format(IMAGE = False, VIDEO = False):
    confirm = input("IMAGE OR VIDEO ?")
    if (confirm.lower() == "IMAGE".lower()):# or confirm == "image"):
        IMAGE = True
        seconds = None
    elif(confirm.lower() == "VIDEO".lower()):
        VIDEO =True
        seconds = input("動画の撮影間隔を入力してください")
    else:
        print("NOT MATCH FORMAT")
        sys.exit()
    print(IMAGE, VIDEO)
    return IMAGE, VIDEO, seconds


"""
IMAGE, VIDEO, seconds = confirm_format()
if IMAGE:
    print("succeeded")
if VIDEO:
    print("video succeeded")
    """

