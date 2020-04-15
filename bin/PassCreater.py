import sys
import os
import PyQt5

# current_path = os.getcwd()
dir_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
# sys.path.append(current_path1)
sys.path.append(dir_path)

from PyQt5.QtWidgets import QApplication
from gui.QT_GUI import *

if __name__ == '__main__':  # 程序的入口
    app = QApplication(sys.argv)
    win = Form()
    win.show()
    sys.exit(app.exec_())
