import sys
import time
import pyautogui
import utils
from PySide6.QtCore import QObject, QSize, QThread, Signal
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QCheckBox, QVBoxLayout


class Worker(QObject):

    finished = Signal()  # give worker class a finished signal
    jiggler = utils.Jiggler()

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)

    def work(self):
        self.jiggler.start_jiggler()
        # utils.test()
        self.finished.emit()  # emit the finished signal when the loop is done

    def stop(self):
        print("stop thread worker")
        self.jiggler.stop_jiggler()  # set the jiggler run condition to False


class MainWindow(QMainWindow):

    # make a stop signal to communicate with the worker in another thread
    stop_signal = Signal()

    def __init__(self):
        super().__init__()

        # Jiggler values
        self.x = 1
        self.y = 1
        self.duration = 1
        self.sleep = 1

        # Buttons
        self.button = QPushButton("Press Me!")
        # self.button.setCheckable(True)
        self.jiggler_checkbox = QCheckBox("Press me!")

        # GUI
        self.setWindowTitle("Mouse Jiggler")
        self.setFixedSize(QSize(200, 100))

        # Thread
        self.thread = QThread()
        self.worker = Worker()
        # connect stop signal to worker
        self.stop_signal.connect(self.worker.stop)
        self.worker.moveToThread(self.thread)

        # connect the worker's finished signal to stop thread
        self.worker.finished.connect(self.thread.quit)
        # connect the worker's finished signal to clean up worker
        self.worker.finished.connect(self.worker.deleteLater)
        # connect thread's finished signal to clean up thread
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.started.connect(self.worker.work)
        self.thread.finished.connect(self.worker.stop)

        self.jiggler_checkbox.stateChanged.connect(self.toogle_jiggle)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.jiggler_checkbox)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def stop_thread(self):
        self.stop_signal.emit()  # emit the finished signal on stop
        self.worker.stop()

    def toogle_jiggle(self, int):
        if self.jiggler_checkbox.isChecked():
            self.thread.start()
        else:
            self.stop_thread()


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
