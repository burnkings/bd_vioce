import json
import os
import sys

import requests
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QPalette, QColor, QAction
from PyQt6.QtWidgets import *

# 百度语音合成API接口


URL = 'http://tts.baidu.com/text2audio'
# 支持的发音人列表
PER_LIST = ['度小美', '度小宇', '度逍遥', '度丫丫']
dict_LIST = {'度小美': 0, '度小宇': 1, '度逍遥': 3, '度丫丫': 4}


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('百度API')
        self.setFixedSize(300, 150)
        self.settings = QSettings("MyCompany", "MyApp")
        self.text1 = self.settings.value("text1", "")
        self.text2 = self.settings.value("text2", "")
        layout = QVBoxLayout()
        self.api = QLineEdit(self.text1)

        def api():
            if self.api.text() == "":
                self.api.setPlaceholderText("请输入API KEY")

        self.api.setPlaceholderText("请输入API KEY")
        layout.addWidget(self.api)
        self.api.textChanged.connect(api)
        self.secret = QLineEdit(self.text2)

        def secret():
            if self.secret.text() == "":
                self.secret.setPlaceholderText("请输入Secret KEY")

        self.secret.setPlaceholderText("请输入Secret KEY")
        layout.addWidget(self.secret)
        self.secret.textChanged.connect(secret)
        button = QPushButton('保存')
        button.clicked.connect(self.save_data)
        layout.addWidget(button)

        button.clicked.connect(self.confirm)

        self.setLayout(layout)

    def save_data(self):
        # 保存数据
        self.settings.setValue("text1", self.api.text())
        self.settings.setValue("text2", self.secret.text())

    def confirm(self):
        # 获取token的server
        baidu_url = r'https://aip.baidubce.com/oauth/2.0/token?'
        grant_type = 'client_credentials'
        # API KEY
        client_id = self.api.text()
        # Secret KEY
        client_secret = self.secret.text()
        # 合成请求token的url
        url = baidu_url + 'grant_type=' + grant_type + '&client_id=' + client_id + '&client_secret=' + client_secret
        res = requests.get(url)
        if res.status_code == 200:
            data = json.loads(res.text)  # 将json格式转换为字典格式
            global token
            token = data['access_token']
            self.close()
        else:
            QMessageBox.about(self, "警告", "密匙不正确")


class TextToSpeech(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = '文字转语音'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 500
        self.initUI()
        self.path = os.path.dirname(os.path.realpath(sys.argv[0]))

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        menubar = self.menuBar()
        batch_convert = menubar.addMenu('批量转换')
        text_convert = QAction('文字转换', self)
        batch_convert.addAction(text_convert)
        text_convert.triggered.connect(self.batch_convert)

        fileset = menubar.addMenu('设置')
        set_file = QAction('百度API', self)
        fileset.addAction(set_file)

        def open_dialog():
            dialog = MyDialog()
            dialog.exec()

        fileset.triggered.connect(open_dialog)
        # 设置背景颜色
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        self.setPalette(palette)
        # 添加标签控件
        label2 = QLabel('选择发音人:', self)
        label2.move(20, 310)
        label3 = QLabel('选择语速:', self)
        label3.move(250, 355)
        label4 = QLabel('选择音调:', self)
        label4.move(250, 310)
        label5 = QLabel('选择音量:', self)
        label5.move(20, 355)

        # 添加文本编辑控件
        def on_text_changed():
            if self.textedit.toPlainText() == "":
                self.textedit.setPlaceholderText("请输入要转换的文字")

        self.textedit = QPlainTextEdit(self)
        self.textedit.setPlaceholderText('请输入要转换的文字')
        self.textedit.setGeometry(20, 30, 460, 280)
        self.textedit.textChanged.connect(on_text_changed)

        # 添加下拉框控件
        self.combobox1 = QComboBox(self)
        self.combobox1.setGeometry(20, 335, 150, 25)
        self.combobox1.addItems(PER_LIST)
        # 语速
        self.combobox2 = QComboBox(self)
        self.combobox2.setGeometry(250, 380, 150, 25)
        self.combobox2.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
        self.combobox2.setCurrentIndex(5)
        # 音调
        self.combobox3 = QComboBox(self)
        self.combobox3.setGeometry(250, 335, 150, 25)
        self.combobox3.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
        self.combobox3.setCurrentIndex(5)
        # 音量
        self.combobox4 = QComboBox(self)
        self.combobox4.setGeometry(20, 380, 150, 25)
        self.combobox4.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
        self.combobox4.setCurrentIndex(5)
        # 添加按钮控件
        self.button1 = QPushButton('单个转换', self)
        self.button1.setGeometry(170, 440, 100, 30)
        self.button1.clicked.connect(self.single_convert)
        # 显示窗口
        self.show()

    def batch_convert(self):
        # 弹出文件选择对话框
        files, file_pyte = QFileDialog.getOpenFileName(self, '选择文件', self.path, '文件类型(*.txt)')
        # 如果没有选择文件，直接返回
        if files == "":
            return
        else:
            # 读取文件
            with open(f'{files}', 'r', encoding='utf8') as f:
                for i in f:
                    self.text = i.strip()
                    self.request()

    def single_convert(self):
        self.text = self.textedit.toPlainText()
        self.request()

    def request(self):
        per = self.combobox1.currentText()
        spd = self.combobox2.currentText()
        pit = self.combobox3.currentText()
        vol = self.combobox4.currentText()
        # 设置请求参数
        data = {
            'tok': token,
            'tex': self.text,
            'per': dict_LIST.get(per),
            'spd': spd,
            'pit': pit,
            'vol': vol,
            'cuid': '123456PYTHON',
            'lan': 'zh',
            'ctp': 1,
            'aue': 3
        }

        # 发送请求
        res = requests.post(URL, data=data)
        # 保存音频文件
        path = self.path + '\\' + f'{self.text}.mp3'
        with open(path, 'wb') as f:
            f.write(res.content)
            return
            # 播放音频文件
        # os.system('mpg123 speech.mp3')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextToSpeech()
    sys.exit(app.exec())
