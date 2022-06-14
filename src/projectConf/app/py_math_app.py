from PyQt5.QtWidgets import QApplication


class PyMathApp(QApplication):
    def __init__(self, sys_argv):
        super(PyMathApp, self).__init__(sys_argv)
