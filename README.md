## bd_vioce

#### description（说明）

It supports Baidu api and single-text conversion and batch conversion. The script is designed with a gui interface, so you can run it directly, but you need to fill in API_KEY and SECRET_KEY in the Settings (there is a bug that every time you run this script, you have to open the Settings first so that your saved information can take effect).

支持百度api，支持单文本转换和批量转换，脚本设计了gui界面，所以直接运行即可，不过需要在设置里填写API_KEY和SECRET_KEY（目前有个bug，每次运行该脚本，都要先点开设置以便自己保存的信息生效）。

#### pack（打包）

To download pyinstaller, run pyinstaller -F -w bd_voice.py on the CLI to package the installer as an exe file

下载pyinstaller，在命令行输入pyinstaller -F -w bd_voice.py 即可打包成exe文件
