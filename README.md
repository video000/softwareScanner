# softwareScanner
+ 软件正版化检查工具
+ 运行后生成一个csv文件，显示软件正版化检查情况。但目前没有维护太多软件清单，随后慢慢补充吧。

环境：python3.8 32位 

## 一、如果需要修改源代码和重新打包，请按以下步骤执行：
0. 修改version 文件，修改自己的version信息，不改也行，随便。
1. pip install gooey
2. pip install pyinstaller
3. pyinstaller -w -F --clean --uac-admin -i program_icon.ico --version-file version softScan.py

## 二、如果仅需要运行python文件，需要安装gooey包：
1. pip install gooey
