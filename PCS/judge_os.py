import platform
def if_Windows_or_Linux():
    system = platform.system()

    if system == "Windows":
        print("I estimate your OS is Windows")
        return True
    elif system == "Linux":
        print("I estimate your OS is Linux")
        return False
    else:
        print(system)
        raise ValueError("サポートされていないOSです。\n使用したいOSがWindowsもしくはLinuxでない場合、main.pyファイルを見直してください。")
