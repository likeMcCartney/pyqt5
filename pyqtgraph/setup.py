from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

from gui.mainwindow import Ui_MainWindow


listX = [0,100]
listY1 = [0,0]
listY2 = [1,1]

for i in range(2, 1000):
    if listX[i-1] == listX[i-2]:
        listX.append(listX[i-1] + 100)
        listY1.append(listY1[i-1])
        listY2.append(listY2[i-1])
    else:
        listX.append(listX[i-1])
        listY1.append(0) if listY1[i-1] == 1 else listY1.append(1)
        listY2.append(0) if listY2[i-1] == 1 else listY2.append(1)
        

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Настройка окна отображения графиков
        self.pyqtgraphWidget.hideAxis('left')
        self.pyqtgraphWidget.setMouseEnabled(y=False, x=False)
        self.pyqtgraphWidget.setXRange(0, listX[len(listX)-1], padding=False)
        # Настройка горизонтальной полосы прокрутки
        self.max_x_scale = listX[len(listX)-1] - listX[0]
        self.x_scale = self.max_x_scale
        self.hScrollBar.setMinimum(listX[0])
        self.hScrollBar.setMaximum(listX[0])
        self.hScrollBar.setPageStep(self.max_x_scale)
        # Добавление функций кнопок и скроллеров
        self.add_functions()
        # Тестовые графики
        for i in range(0, 5):
            self.plot(listX, listY1, -((2*i)*2))
            self.plot(listX, listY2, -((2*i+1)*2))

    def plot(self, x, y, yoffs=0):
        lx = list(x)
        ly = list(y)
        for i in range(0, len(ly)):
            ly[i] += yoffs
        self.pyqtgraphWidget.plot(lx, ly)

    def change_x_scale(self, step):
        x_min = self.hScrollBar.minimum()
        x_max = self.hScrollBar.maximum()
        page_step = int(self.hScrollBar.pageStep() * step)
        if page_step > self.max_x_scale:
            page_step = self.max_x_scale
        x_max = self.max_x_scale - page_step - x_min
        self.x_scale = page_step
        self.hScrollBar.setMinimum(x_min)
        self.hScrollBar.setMaximum(x_max)
        self.hScrollBar.setPageStep(page_step)
        self.pyqtgraphWidget.setXRange(0, page_step, padding=False)

    def scroll_x(self):
        x_min = self.hScrollBar.value()
        x_max = x_min + self.x_scale
        if x_max > 50000:
            x_max = 50000
            x_min = 50000 - self.x_scale
        self.pyqtgraphWidget.setXRange(x_min, x_max, padding=False)
    
    def add_functions(self):
        self.scaleIncButton.clicked.connect(lambda: self.change_x_scale(1.4))
        self.scaleDecButton.clicked.connect(lambda: self.change_x_scale(0.7))
        self.hScrollBar.valueChanged.connect(lambda: self.scroll_x())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
