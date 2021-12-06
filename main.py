import sys
import time
import pyautogui

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from beginUI import *
from MyQQ import *
import cutImage
import pyscreenshot as ImageGrab

class MyWindow(QMainWindow, Ui_dialog):
    # 用于窗口间消息传递
    mySignal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)
        self.pushButton_3.clicked.connect(self.tools)

    def login(self):
        '''
        登录
        :return:
        '''
        box = QMessageBox()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        try:
            a = self.users[username]
        except Exception as e:
            box.setText("账号或密码错误！！！")
            box.exec_()
        else:
            if a == password:
                # username为要发生的消息的内容
                self.mySignal.emit(username)
                myWin.close()
                time.sleep(1)
                myQQ.show()
            else:
                box.setText("账号或密码错误！！！")
                box.exec_()
        pass

    def register(self):
        '''
        注册
        :return:
        '''
        box = QMessageBox()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username and password:
            self.users[username] = password
            self.mySignal.emit(username)
            myWin.close()
            box.setText("注册成功！！")
            box.setStandardButtons(QMessageBox.Ok)  # QMessageBox显示的按钮
            box.button(QMessageBox.Ok).animateClick(1000)  # t时间后自动关闭(t单位为毫秒)
            box.exec_()
            myQQ.show()
        else:
            box.setText("账号或密码错误！！！")
            box.exec_()

    def tools(self):
        cut_Image.show()



class MyQQ(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyQQ, self).__init__(parent)
        self.setupUi(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timeupdate)
        self.timer.start(100)
        # 用于接收登录窗口发送的数据
        myWin.mySignal.connect(self.getDialogSignal)

    def timeupdate(self):
        T = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.label_2.setText(T)

    def getDialogSignal(self, connect):
        self.label.setText(connect)

class CutImage(QMainWindow, cutImage.Ui_Form):
    def __init__(self, parent=None):
        super(CutImage, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.cut)

    def cut(self):
        im = ImageGrab.grab()
        im.save("./lj.jpg")
        im.close()

if __name__ == '__main__':
    # 实现不同分辨率下的电脑上的相同显示
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    myQQ = MyQQ()
    cut_Image = CutImage()
    sys.exit(app.exec_())
