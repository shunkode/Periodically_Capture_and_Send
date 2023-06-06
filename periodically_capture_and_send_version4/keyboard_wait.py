import time

from judge_os import if_Windows_or_Linux



if if_Windows_or_Linux():
    print("I guess you are using Windows")
    import keyboard
    #from capture import wait_keyboard_with_Windows, operate_camera, Capture, Capture_regularly, execution_Capture_regularly

    def wait_keyboard_with_Windows(wait_time):
        wait_start_time = time.time()
        print("You should push escape key if you want to finish")
        while ((time.time() - wait_start_time) < wait_time):
            if keyboard.is_pressed("escape"):
                print("I COMPLETE THIS WORK!!! \nGOOD JOB FOR TODAY!!!")
                return False
        print("finish waiting keyboard")
        return True
            
            
        
            

elif not if_Windows_or_Linux():
    print("I guess you are using Linux")
    import evdev
    import select

    # target_string（対象とする文字列）の中に、search_string（探したい文字列）が含まれているか判定するプログラム
    def if_contains_string(search_string, target_string):
        search_string = search_string.lower()
        target_string = target_string.lower()

        if search_string in target_string:
            return True
        else:
            return False

    # 接続しているUSBデバイスのパスを探す & イベントを取得するデバイスとして指定するプログラム
    def search_and_use_usb_device(search_device_name):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for dev in devices:
            print(dev.path, dev.name)#, dev.phys)
            if if_contains_string(search_device_name, dev.name):
                device_path = dev.path
        print("device_path: ", device_path)
        device = evdev.InputDevice(device_path)
        return device

    ## Usage(search_and_use_usb_device("device_name  ex:keyboard, mouse, etc..."))


    def wait_keyboard_with_Linux(wait_time):
        keyboard = search_and_use_usb_device("keyboard")
        # Escapeキーのコードを取得
        esc_keycode = evdev.ecodes.KEY_ESC

        # 3秒間入力待ちする
        timeout = wait_time

        # イベント待機ループ
        while True:
            # イベントを取得
            r, w, x = select.select([keyboard], [], [], timeout)
            if keyboard in r:
                events = keyboard.read()
                for event in events:
                    if event.type == evdev.ecodes.EV_KEY and event.code == esc_keycode and event.value == 1:
                        print("Escape key pressed")
                        return False
                        #break
            else:
                print("Timeout occurred")
                return True
                #break

if __name__ == "__main__":
    keyboard = search_and_use_usb_device("keyboard")
    wait_keyboard_with_Linux(keyboard)
    
"""
## Usage(if_contains_string, search_and_use_usb_device, wait_keyboard)
keyboard = search_and_use_usb_device("keyboard")
wait_keyboard(wait_time)
"""


def keyboard_wait(scheduled_time, keyboard=None):
    interval = scheduled_time - time.time()
    if interval < 10:
        rest_time = interval * 7 / 10
        keyboard_wait_time = interval / 10
        print(f"WE WILL WAIT {keyboard_wait_time} seconds after {rest_time} SECONDS. \nIF YOU WANT TO FINISH SENDING, YOU SHOULD PUSH ESCAPE in that time. \nI WON'T REPEAT THIS WORK.")
        time.sleep(rest_time)
        if if_Windows_or_Linux():
            wait_keyboard_with_Windows(keyboard_wait_time)
        if not if_Windows_or_Linux():
            wait_keyboard_with_Linux(keyboard, keyboard_wait_time)

    
    elif 10 <= interval < 30:
        rest_time = interval * 3 / 10
        keyboard_wait_time = interval / 10
        print(f"WE WILL WAIT {keyboard_wait_time} seconds after {rest_time} SECONDS. \nIF YOU WANT TO FINISH SENDING, YOU SHOULD PUSH ESCAPE in that time. \nI'll conduct this work twice.")
        for i in range(2):
            time.sleep(rest_time)
            if if_Windows_or_Linux():
                waiting_keyboard = wait_keyboard_with_Windows(keyboard_wait_time)
                if not waiting_keyboard:
                    break
                
            if not if_Windows_or_Linux():
                waiting_keyboard = wait_keyboard_with_Linux(keyboard_wait_time)
                if not waiting_keyboard:
                    break

                #wait_keyboard_with_Linux(keyboard, keyboard_wait_time)
                #break
            #else:
            #    continue
            


    elif 30 <= interval < 60:
        rest_time = interval * 2 / 10
        keyboard_wait_time = interval / 10
        print(f"WE WILL WAIT {keyboard_wait_time} seconds after {rest_time} SECONDS. \nIF YOU WANT TO FINISH SENDING, YOU SHOULD PUSH ESCAPE in that time. \nI'll conduct this work third time.")
        for i in range(3):
            time.sleep(rest_time)
            if if_Windows_or_Linux():
                waiting_keyboard = wait_keyboard_with_Windows(keyboard_wait_time)
                if not waiting_keyboard:
                    break
                
            if not if_Windows_or_Linux():
                waiting_keyboard = wait_keyboard_with_Linux(keyboard_wait_time)
                if not waiting_keyboard:
                    break
                #wait_keyboard_with_Linux(keyboard, keyboard_wait_time)
                #break
            #else:
            #    continue
    
    elif 60 <= interval < 200:
        rest_time = interval  / 10
        keyboard_wait_time = interval / 10
        print(f"WE WILL WAIT {keyboard_wait_time} seconds after {rest_time} SECONDS. \nIF YOU WANT TO FINISH SENDING, YOU SHOULD PUSH ESCAPE in that time. \nI'll conduct this work fourth time.")
        for i in range(4):
            time.sleep(rest_time)
            if if_Windows_or_Linux():
                #wait_keyboard_with_Windows(keyboard_wait_time)
                waiting_keyboard = wait_keyboard_with_Windows(keyboard_wait_time)
                if not waiting_keyboard:
                    break
                """
                else:
                    continue
                break
                """
                
            if not if_Windows_or_Linux():
                waiting_keyboard = wait_keyboard_with_Linux(keyboard_wait_time)
                if not waiting_keyboard:
                    break
                #wait_keyboard_with_Linux(keyboard, keyboard_wait_time)
                #break
            """
            else:
                print("T")
                continue
                print("F")
            break
            """
            

    elif 200 <= interval:
        rest_time = 40
        keyboard_wait_time = 10
        print(f"WE WILL WAIT {keyboard_wait_time} seconds after {rest_time} SECONDS. \nIF YOU WANT TO FINISH SENDING, YOU SHOULD PUSH ESCAPE in that time.")
        while (scheduled_time - time.time()) >= 60:
            time.sleep(rest_time)
            if if_Windows_or_Linux():
                waiting_keyboard = wait_keyboard_with_Windows(keyboard_wait_time)
                if not waiting_keyboard:
                    break
            if not if_Windows_or_Linux():
                waiting_keyboard = wait_keyboard_with_Linux(keyboard_wait_time)
                if not waiting_keyboard:
                    break
                #wait_keyboard_with_Linux(keyboard, keyboard_wait_time)
                #break
            #else:
            #    continue
    
    if waiting_keyboard:
        return True
    if not waiting_keyboard:
        return False

import sys
def determine_scheduled_time(scheduled_time, interval, DAY, HOUR, MINUTE, SECOND):
    if (DAY and HOUR) or (DAY and MINUTE) or (DAY and SECOND) or (HOUR and MINUTE) or (HOUR and SECOND) or (MINUTE and SECOND):
        print("Only one of DAY, HOUR, MINUTE and SECOND should be True")
    if SECOND:
        print("I guess you input SECOND")

    if DAY:
        interval = interval * 86400
        print("I guess you input DAY")
    elif HOUR:
        interval = interval * 3600
        print("I guess you input HOUR")
    elif MINUTE:
        interval = interval * 60
        print("I guess you input MINUTE")
    elif SECOND:
        print("I guess you input SECOND")
    else:
        print("NOT MATCH FORMAT!")
        sys.exit()
    scheduled_time =scheduled_time + interval
    return scheduled_time

"""
## Usage
scheduled_time = scheduled_time = determine_scheduled_time(scheduled_time, interval, DAY, HOUR, MINUTE, SECOND)
"""