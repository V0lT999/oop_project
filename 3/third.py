import sys
import xlrd, xlwt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QAction, qApp, QMainWindow, QTableWidget, QTableWidgetItem, \
        QGridLayout, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QRect


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.table = QTableWidget(self)
        self.initUI()

    def initUI(self):
        self.resize(1000, 700)
        self.center()
        self.setWindowTitle('Library')
        self.setWindowIcon(QIcon('../resources/library_ico.png'))

        saveAction = QAction(QIcon('../resources/save_ico.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)

        newAction = QAction(QIcon('../resources/new_ico.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.new_book)

        printAction = QAction(QIcon('../resources/print_ico.png'), 'Print', self)
        printAction.setShortcut('Ctrl+P')
        # printAction.triggered.connect(qApp.quit)

        exitAction = QAction(QIcon('../resources/exit_ico.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(newAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(printAction)

        #self.setMinimumSize(QSize(200, 80))
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
        self.table = self.create_table()

        self.search_line = QLineEdit(self)
        self.search_button = QPushButton('Search')
        self.autor_box = QComboBox(self)
        for rownum in range(self.table.rowCount()):
            self.autor_box.addItem(self.table.item(rownum, 1).text())

        grid_layout.addWidget(self.table, 0, 0)
        grid_layout.addWidget(self.search_line, 1, 0)
        grid_layout.addWidget(self.search_button, 1, 1)
        grid_layout.addWidget(self.autor_box, 1, 2)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save(self):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Sheet1')
        for colnum in range(self.table.columnCount()):
            ws.write(0, colnum, self.table.takeHorizontalHeaderItem(colnum).text())
        for rownum in range(self.table.rowCount()):
            for colnum in range(self.table.columnCount()):
                ws.write(rownum + 1, colnum, self.table.item(rownum, colnum).text())
        wb.save('../resources/books.xls')
        print("success")

    def create_table(self):
        #self.table = QTableWidget(self)
        rb = xlrd.open_workbook('../resources/books.xls', formatting_info=False)
        sheet = rb.sheet_by_index(0)
        self.table.setColumnCount(sheet.ncols)
        self.table.setRowCount(sheet.nrows - 1)
        self.table.setHorizontalHeaderLabels(sheet.row_values(0))
        for rownum in range(1, sheet.nrows):
            row = sheet.row_values(rownum)
            for colsnum in range(sheet.ncols):
                self.table.setItem(rownum - 1, colsnum, QTableWidgetItem(row[colsnum]))

        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        return self.table

    def new_book(self):
        self.application = Window_new_book()
        self.application.show()


class Window_new_book(QWidget):
    def __init__(self):
        super(Window_new_book, self).__init__()

        # self.resize(300, 500)
        # self.center()
        # self.setWindowTitle('Library')
        # self.setWindowIcon(QIcon('../resources/library_ico.png'))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.name = QLineEdit(self.central_widget)
        self.name.setGeometry(QRect(10, 10, 291, 31))
        self.name.setObjectName("Name")
        self.lineEdit_2 = QLineEdit(self.central_widget)
        self.lineEdit_2.setGeometry(QRect(10, 50, 291, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QLineEdit(self.central_widget)
        self.lineEdit_3.setGeometry(QRect(10, 90, 291, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QLineEdit(self.central_widget)
        self.lineEdit_4.setGeometry(QRect(10, 130, 291, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())