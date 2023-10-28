from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys


def get_scr_width():
    desktop = QApplication.desktop()
    geometry = desktop.screenGeometry()
    w = geometry.width()
    return w


def get_scr_height():
    desktop = QApplication.desktop()
    geometry = desktop.screenGeometry()
    h = geometry.height()
    return h


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.win_width = 600  # Ширина окна
        self.win_height = 800  # Высота окна
        # Настройка главного текстового поля
        self.editor = QTextEdit()
        self.editor.setAcceptRichText(False)

        self.path = None  # Путь к открытому файлу

        layout = QVBoxLayout()  # Здесь расположен editor
        layout.addWidget(self.editor)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.statusbar = QStatusBar()  # Добавление статусбара
        self.setStatusBar(self.statusbar)

        file_menu = self.menuBar().addMenu("File")  # Добавление меню "Файл"

        open_file_action = QAction(QIcon("images\\openfile.png"), "Open...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.openfile)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon("images\\savefile.png"), "Save...", self)
        save_file_action.setStatusTip("Save file")
        save_file_action.triggered.connect(self.savefile)
        file_menu.addAction(save_file_action)

        saveas_file_action = QAction(QIcon("images\\savefileas.png"), "Save As...", self)
        saveas_file_action.setStatusTip("Save file to another path")
        saveas_file_action.triggered.connect(self.savefileas)
        file_menu.addAction(saveas_file_action)

        print_action = QAction(QIcon("images\\printfile.png"), "Print...", self)
        print_action.setStatusTip("Print this file")
        print_action.triggered.connect(self.printfile)
        file_menu.addAction(print_action)

        file_menu.addSeparator()
        exit_action = QAction(QIcon("images\\exit.png"), "Exit", self)
        exit_action.setStatusTip("Quit Simple Notes")
        exit_action.triggered.connect(self.exit)
        file_menu.addAction(exit_action)

        edit_menu = self.menuBar().addMenu("Edit")  # Добавление меню "Правка"

        undo_action = QAction(QIcon("images\\undo.png"), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        self.editor.addAction(undo_action)

        redo_action = QAction(QIcon("images\\redo.png"), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        self.editor.addAction(redo_action)

        cut_action = QAction(QIcon("images\\cut.png"), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)
        self.editor.addAction(cut_action)

        copy_action = QAction(QIcon("images\\copy.png"), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
        self.editor.addAction(copy_action)

        paste_action = QAction(QIcon("images\\paste.png"), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)
        self.editor.addAction(paste_action)

        select_action = QAction(QIcon("images\\selectall.png"), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)
        self.editor.addAction(select_action)

        credits_menu = self.menuBar().addMenu("Credits")  # Добавление меню титров
        open_credits = QAction(QIcon("images\\credits.png"), "Credits...", self)
        open_credits.setStatusTip("Show credits")
        open_credits.triggered.connect(self.opencredits)
        credits_menu.addAction(open_credits)

        file_menu.show()
        edit_menu.show()
        credits_menu.show()
        self.window_personalize()
        self.show()  # По умолчанию окно скрыто
        self.statusbar.showMessage("Ready", 3000)  # Сообщение о старте программы
        self.editor.textChanged.connect(self.getWordCount)

    def getWordCount(self):  # Счётчик слов
        text = self.editor.toPlainText()
        words = len(text.split())
        if words:
            self.statusbar.showMessage(f"Words: {str(words)}", 3000)
        else:
            self.statusbar.clearMessage()

    def openfile(self):  # Открытие файла
        path, meta = QFileDialog.getOpenFileName(self)
        if path:
            try:
                file = open(path, "r", encoding="utf-8")
            except FileNotFoundError:  # Это перестраховка, т.к. QFileDialog не откроет несуществующий файл
                dialog = QMessageBox(self)
                dialog.setText(f"Can not open {path}.")
                dialog.show()
            else:
                self.editor.setPlainText(file.read())  # Собственно открытие файла
                self.setWindowTitle("Simple Notes - %s" % (os.path.basename(path)))
                self.path = path

    def savetopath(self, path):  # Сохранение файла в заданный путь
        file = open(path, "w", encoding="utf-8")  # Если файл не существует, он будет создан
        file.write(self.editor.toPlainText())
        self.setWindowTitle("Simple Notes - %s" % (os.path.basename(path)))
        self.path = path

    def savefile(self):  # Обычное сохранение файла
        if self.path is None:
            # Если в переменной path ничего нет, то "сохраняем как"
            return self.savefileas()
        self.savetopath(self.path)  # Вызов базовой функции сохранения в путь

    def savefileas(self):  # Расширенное сохранение файла
        path, meta = QFileDialog.getSaveFileName(self)
        if path:
            self.savetopath(path)  # Вызов базовой функции сохранения в путь
        else:
            return

    def printfile(self):  # Печать файла
        printdialog = QPrintDialog()
        if printdialog.exec_():
            self.editor.print_(printdialog.printer())

    def opencredits(self):
        creditsdialog = QMessageBox(self)
        c = """Made by: Nikita 'Nuke' Karachentsev
        \n
        \nIf you want to support us,
        \nwe are here: vk.com/super_nuke.
        \nThanks for using 'Simple Notes'!"""
        creditsdialog.setText(c)
        creditsdialog.setWindowTitle("Credits")
        creditsdialog.setWindowIcon(QIcon("images\\credits.png"))
        creditsdialog.show()

    def exit(self):
        exitdialog = QMessageBox(self)
        q = exitdialog.question(self, "Exit", "Do you want to exit?", exitdialog.Yes | exitdialog.No)
        exitdialog.show()
        if q == exitdialog.Yes:
            sys.exit()
        else:
            exitdialog.close()

    def window_personalize(self):  # Настройка параметров окна
        # Меняем заголовок окна
        if self.path:
            self.setWindowTitle("Simple Notes - %s" % (os.path.basename(self.path)))
        else:
            self.setWindowTitle("Simple Notes - Untitled")
        # Находим размеры экрана для отображения окна по центру
        central_x = get_scr_width() // 2 - self.win_width // 2
        central_y = get_scr_height() // 2 - self.win_height // 2
        self.setGeometry(central_x, central_y, self.win_width, self.win_height)
        self.setWindowIcon(QIcon("images\\simplenotes.png"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Simple Notes")
    window = Window()
    app.exec_()
