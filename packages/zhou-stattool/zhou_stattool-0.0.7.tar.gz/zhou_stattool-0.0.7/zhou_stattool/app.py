import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from zhou_stattool.mainwindow import Ui_Dialog
from zhou_stattool.roomdata_window_main import RoomdataMainWindow


class AppMainWindow(QMainWindow):
    def __init__(self):
        super(AppMainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.goto_roomdata_state)
        self.ui.pushButton_2.clicked.connect(self.goto_operateroom_state)

    def goto_roomdata_state(self):
        self.roomdata_window = RoomdataMainWindow()
        self.roomdata_window.show()


    def goto_operateroom_state(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()