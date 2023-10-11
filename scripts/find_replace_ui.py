import sys
import unreal
from PySide6.QtWidgets import QWidget, QApplication, QLineEdit, QPushButton, QVBoxLayout, QCheckBox
#from PyQt6.QtWidgets import QApplication, QWidget


class FindReplaceWidget(QWidget):
    def __init__(self, parent=None):
        super(FindReplaceWidget, self).__init__(parent)
        self.setWindowTitle("Material Find and Replace")
        self.create_widgets()

    def create_widgets(self):
        vbox = QVBoxLayout(self)
        material_path = QLineEdit("Path to Material")
        vbox.addWidget(material_path)

        directory_path = QLineEdit("Path to Directory to Search Within")
        vbox.addWidget(directory_path)

        recursive_search = QCheckBox()
        vbox.addWidget(recursive_search)

        submit_btn = QPushButton("Find and Replace")
        vbox.addWidget(submit_btn)


if __name__ == "__main__":
    app = None

    if not QApplication.instance():
        print("no instance")
    
    '''
    # pyqt
    if not QApplication.instance():
        app = QApplication(sys.argv)

    window = QWidget()
    window.show()

    # Start the event loop.
    #app.exec()
    '''


    # pyside
    app = None
    if not QApplication.instance():
        app = QApplication(sys.argv)
    
    widget = FindReplaceWidget()
    widget.show()
    app.exec_()
    unreal.parent_external_window_to_slate(widget.winId())