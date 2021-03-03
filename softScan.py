# !/usr/bin/env Python
# # coding=utf-8
from __future__ import unicode_literals
from __future__ import print_function
from time import sleep
from gooey import Gooey, GooeyParser
# from gooey.gui.components import modals
import ctypes,sys,os,codecs,winreg,time
from colored import stylize, attr, fg 
# 白名单免费
expec_soft_ok = [
    "WPS Office 2016专业版",
    "Firefly",
    "360压缩",
    "7-Zip",
    "Adobe Reader",
    "Sursen Reader",
    "CAJ全文浏览器",
    "亚信安全防毒墙",
    "北信源终端管理",
]
# 白名单付费
expec_soft_ques = [
    "Python",
    "Acrobat pro",
    "Microsoft Visio",
    "Office 2013",
    "Microsoft Visio",
    "WinRAR",
    "Indesign CS6",
    "Dreamwaver CS6",
    "Flash pro CS6",
    "Fireworks CS6",
    "Premier pro CS6",
    "After Effects CS6",
    "Photoshop CS6",
    "Illustrator CS6",
]
#window 默认的一些常用系统软件
Windows_Default_Apps =[
    'Microsoft Visual',
    'Microsoft .',
    'Intel(R)',
    'Realtek',
    'NVIDIA',
    'Lenovo',
    'EasyConnect',
]
#软件识别后的提示信息
soft_tips={
    1:"白名单内免费软件，放心使用！",
    2:"白名单内付费，如盗版使用，请卸载!",
    3:"白名单外软件，请自行核查是否获得授权！如盗版使用，请卸载！",
}


def coding_fix(func):
    """
    编码库修复装饰器
    """
    def wrapper(*args, **kwargs):
        if sys.stdout.encoding != 'UTF-8':
            sys.stdout = codecs.getwriter('UTF-8')(sys.stdout.buffer,'strict')
        if sys.stderr.encoding != 'UTF-8':
            sys.stderr = codecs.getwriter('UTF-8')(sys.stderr.buffer,'strict')
        f = func(*args, **kwargs)
        return f
    return wrapper

def duration(func):
    """
    计时装饰器
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)
        print(str("扫描完成， 用时  ") + str(int(time.time()-start)) + "秒！")
        return f
    return wrapper


def is_windows_default_apps(soft):
    for i in Windows_Default_Apps:
        if soft.startswith(i):
            return True
    return False

sub_key = [
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
    "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
]
software_name = []

def is_legal(s):
    """
    判断软件是白名单内免费、付费还是白名单外软件。
    """
    for i in expec_soft_ok:
        if s.find(i) != -1:
            return 1
    for j in expec_soft_ques:
        if s.find(j) != -1:
            return 2

    return 3

def display_and_save():
    with open("软件清单.csv", "w") as f:
        for soft in software_name:
            islegal = is_legal(soft)
            colored_print(soft+soft_tips[islegal],islegal)
    
def is_admin():
    try:
        ctypes.windll.shell32.IsUserAnAdmin()
        return True
    except:
        return False

def colored_print(str,type):
    if type ==2:
        print(stylize(str,fg('yellow')))
    elif type ==3:
        print(stylize(str,fg('red')))
    elif type == 0:
        print(stylize(str,fg('black')),attr('bold'))
    elif type == -1:
        print(stylize(str,fg('red')),attr('bold'))
    else :
        print(str)
    # print(type,str)
    sys.stdout.flush()

def software_scan():
    for i in sub_key:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, i, 0, winreg.KEY_ALL_ACCESS)
            for j in range(0, winreg.QueryInfoKey(key)[0] - 1):
                try:
                    key_name = winreg.EnumKey(key, j)
                    key_path = i + "\\" + key_name
                    each_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,key_path,0,winreg.KEY_ALL_ACCESS,)
                    DisplayName, REG_SZ = winreg.QueryValueEx(each_key, "DisplayName")
                    DisplayName = DisplayName.replace("\n", "")
                    if not is_windows_default_apps(DisplayName):
                        software_name.append(DisplayName)                  
                except:
                        pass
        except WindowsError:
            pass


@Gooey(
    program_name=u"审计部软件扫描程序",
    disable_progress_bar_animation=True,
    language="chinese",
    clear_before_run=True,
    auto_start=True,
    richtext_controls=True,
    show_success_modal=False,
    show_restart_button=False,
    image_dir="./",
)
@coding_fix
def main():
    parser = GooeyParser(prog="安装软件扫描程序")
    _ = parser.parse_args(sys.argv[1:])
    if is_admin():
        software_scan()
        display_and_save()
        colored_print("\n软件清单获取成功！", 0)
        colored_print("请将本目录下生成的'软件清单.txt'文件通过OA发送!", 0)
        # os.system("Rundll32.exe Shell32.dll,Control_RunDLL appwiz.cpl,,0")
        
    else:
        colored_print("运行错误，请用管理员模式重新运行!", -1)

    



if __name__ == "__main__":
    main()
    
    
