import sys
import os
import json

dir_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(dir_path)

from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtWidgets import QApplication
from urllib.parse import urlparse

import sqlite3
import uuid
import time
import getpass
import pyperclip
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(426, 258)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../pic/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(170, 170, 90, 40))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(60, 50, 351, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 50, 54, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 110, 331, 41))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(60, 80, 351, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 10, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(190, 10, 131, 31))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 426, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEdit, self.pushButton)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pass Creater"))
        self.pushButton.setText(_translate("MainWindow", "查询"))
        self.label.setText(_translate("MainWindow", "网址:"))
        self.label_2.setText(_translate("MainWindow", "状态信息"))
        self.label_3.setText(_translate("MainWindow", "密码:"))
        self.pushButton_2.setText(_translate("MainWindow", "初始化数据库"))
        self.label_4.setText(_translate("MainWindow", "如未初始化数据库请先"))


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


def Process_entry(url):
    original_url = url  # 体验无GUI请使用input函数
    # print("执行了Process_entry", url, original_url)
    calculate_url = character(original_url=original_url)
    if calculate_url == 1:
        return ["请不要使用非url记录!", 2]
    else:
        Call = Query_Call(calculate_url=calculate_url, original_url=original_url)
        return Call


def Inexistence_Call(calculate_url, original_url):  # 不存在调用
    C_uuid = str(uuid.uuid1())[0:8]
    D_uuid = str(uuid.uuid4())[-12:]
    conn = sqlite3.connect(user_config_json["DBPath"])
    cursor = conn.cursor()
    insert_basetable_sql = sys_config_json["insert_basetable_sql"].format(C_uuid,
                                                                          time.strftime("%Y-%m-%d", time.localtime()),
                                                                          time.strftime("%H:%M:%S", time.localtime()),
                                                                          original_url,
                                                                          calculate_url, getpass.getuser())

    insert_passtable_sql = sys_config_json["insert_passtable_sql"].format(C_uuid, D_uuid, 1)
    clip_copy(PassWord=D_uuid)
    cursor.execute(insert_basetable_sql)
    cursor.execute(insert_passtable_sql)
    cursor.close()
    conn.commit()
    conn.close()
    # print("执行了Inexistence_Call")
    return D_uuid


def Exist_Call(calculate_url, original_url):  # 存在调用
    conn = sqlite3.connect(user_config_json["DBPath"])
    cursor = conn.cursor()
    select_basetable_sql = sys_config_json["select_basetable_sql"].format(calculate_url)
    cursor.execute(select_basetable_sql)
    rows = cursor.fetchall()
    Call_uuid = rows[0][0]
    cursor.close()
    conn.commit()
    conn.close()
    # print("执行了Exist_Call")
    return Query_PassWord(Call_uuid=Call_uuid)


def Query_Call(calculate_url, original_url):
    # print("收到了", calculate_url)
    conn = sqlite3.connect(user_config_json["DBPath"])
    cursor = conn.cursor()
    select_basetable_sql = sys_config_json["select_basetable_sql"].format(calculate_url)
    cursor.execute(select_basetable_sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()

    if len(rows) > 0:
        return [Exist_Call(calculate_url=calculate_url, original_url=original_url), 1]
    else:
        return [Inexistence_Call(calculate_url=calculate_url, original_url=original_url), 0]


def Query_PassWord(Call_uuid):
    select_passtable_sql = sys_config_json["select_passtable_sql"].format(Call_uuid)
    conn = sqlite3.connect(user_config_json["DBPath"])
    cursor = conn.cursor()
    cursor.execute(select_passtable_sql)
    rows = cursor.fetchall()
    PassWord = rows[0][1]
    clip_copy(PassWord=PassWord)
    cursor.close()
    conn.commit()
    conn.close()
    return rows[0][1]


def clip_copy(PassWord):
    pyperclip.copy(PassWord)
    pyperclip.paste()


def init_database():
    conn = sqlite3.connect(user_config_json["DBPath"])
    create_basetable_sql = sys_config_json["create_basetable_sql"]
    create_passtable_sql = sys_config_json["create_passtable_sql"]
    cursor = conn.cursor()
    cursor.execute(create_basetable_sql)
    cursor.execute(create_passtable_sql)
    cursor.close()
    conn.commit()
    conn.close()


def character(original_url):
    # print("char收到了prigurl",original_url)
    res = urlparse(original_url)
    # print(res)
    # print("执行了character", res.netloc)
    if len(res.netloc) > 0:
        return res.netloc

    else:
        return 1


def get_user_config():
    with open("../config/user_config.json", 'r') as load_json:
        user_json = json.load(load_json)
    return user_json


def get_sys_config():
    with open("../config/sys_config.json", 'r') as load_json:
        sys_json = json.load(load_json)
    return sys_json


user_config_json = get_user_config()

sys_config_json = get_sys_config()

if __name__ == '__main__':  # 程序的入口
    app = QApplication(sys.argv)
    win = Form()
    win.show()
    sys.exit(app.exec_())
