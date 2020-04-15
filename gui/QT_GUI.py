from bin.hinge_program import *
from PyQt5.QtWidgets import QMainWindow
from gui.QT_file import Ui_MainWindow  # 加载我们的布局
import sqlite3
from bin.check_config import user_config_json, sys_config_json


class Form(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.setupUi(self)  # 初始化ui

        self.pushButton.clicked.connect(self.Process_Enter)
        self.pushButton_2.clicked.connect(self.init_database)

    def Change_Label(self, text):
        self.label_2.setText(text)

    def Process_Enter(self):
        url = self.lineEdit.text()
        # print(url)
        PassInfo = Process_entry(url=url)
        Pass = PassInfo[0]
        State = PassInfo[1]
        if State == 0:
            # print("执行了lineEdit_1", Pass)
            self.lineEdit_2.setText(Pass)
            self.Change_Label(text="记录不存在!已经为您创建新密码")
        if State == 2:
            self.lineEdit_2.setText("请不要使用非url记录!")
            # print("执行了lineEdit_2", Pass)
            self.Change_Label(text="记录不存在!请不要使用非url记录!")
        if State == 1:
            self.lineEdit_2.setText(Pass)
            self.Change_Label(text="记录存在,密码已经为您复制到剪切板")

    def init_database(self):
        conn = sqlite3.connect(user_config_json["DBPath"])
        create_basetable_sql = sys_config_json["create_basetable_sql"]
        create_passtable_sql = sys_config_json["create_passtable_sql"]
        cursor = conn.cursor()
        cursor.execute(create_basetable_sql)
        cursor.execute(create_passtable_sql)
        cursor.close()
        conn.commit()
        conn.close()