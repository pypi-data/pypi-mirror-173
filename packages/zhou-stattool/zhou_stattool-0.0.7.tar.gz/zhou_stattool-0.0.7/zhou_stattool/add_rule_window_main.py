from PyQt5.QtWidgets import QDialog, QAbstractItemView, QMessageBox
from PyQt5.QtCore import QModelIndex
from zhou_stattool.add_rule_window import Ui_Dialog
from typing import List, Tuple


class AddRuleMainWindow(QDialog):
    def __init__(self, headers, title=None, selected_index=None):
        super(AddRuleMainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.header_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.header = headers
        self.title = title
        self.selected_index = selected_index
        self.ui.ok_btn.clicked.connect(self.close_window)
        for item in headers:
            self.ui.header_widget.addItem(item)
        if title and selected_index:
            self.ui.lineEdit.setText(title)
            for index in selected_index:
                item = self.ui.header_widget.item(index)
                item.setSelected(True)

    def close_window(self):
        if self.title and self.selected_index and (not self.ui.lineEdit.text() or not self.ui.header_widget.selectedIndexes()):
            QMessageBox.critical(self, '错误', '请输入修正后的规则名并选择对应项')
        else:
            self.done(QDialog.Accepted)
            self.close()

    def get_result(self) -> Tuple[str, List[QModelIndex]]:
        return self.ui.lineEdit.text(), self.ui.header_widget.selectedIndexes()