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

step = 2
listX2_ = [0,100,400,800,1200,15000,20000,30000,40000]
listX2 = [0]
listY3_1 = [0.5]
listY3_2 = [0.5]
for val in listX2_:
    if val == 0:
        listX2.append(step)
        listY3_1.append(0)
        listY3_2.append(1)
        continue
    listX2.append(val)
    prevY3_1 = listY3_1[-1]
    prevY3_2 = listY3_2[-1]
    listY3_1.append(prevY3_1)
    listY3_2.append(prevY3_2)
    listX2.append(val+step)
    listY3_1.append(prevY3_2)
    listY3_2.append(prevY3_1)
listX2.append(listX[-1])
listY3_1.append(listY3_1[-1])
listY3_2.append(listY3_2[-1])


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # Настройка окна отображения графиков
        self.pyqtgraphWidget.hideAxis('left')
        self.pyqtgraphWidget.setMouseEnabled(y=False, x=False)
        self.pyqtgraphWidget.setXRange(0, listX[len(listX)-1], padding=False)
        self.pyqtgraphWidget.setYRange(-19, 2, padding=False)
        # Бесконечная линия
        self.infinite_line = pg.InfiniteLine(pos=100, movable=True)
        self.pyqtgraphWidget.addItem(self.infinite_line)
        # Получение объектов, отображаемых на графике
        view_box = self.pyqtgraphWidget.getViewBox()
        for child in view_box.allChildren():
            print(child)
        # Текст
        text = pg.TextItem(text='XYZ')
        self.pyqtgraphWidget.addItem(text)
        # Настройка горизонтальной полосы прокрутки
        self.max_x_scale = listX[len(listX)-1] - listX[0]
        self.x_scale = self.max_x_scale
        self.hScrollBar.setMinimum(listX[0])
        self.hScrollBar.setMaximum(listX[0])
        self.hScrollBar.setPageStep(self.max_x_scale)
        # Настройка вертикальной полосы прокрутки
        self.y_max = 2
        self.y_min = -1
        # Добавление функций кнопок и скроллеров
        self.add_functions()
        # Тестовые графики
        self.plot(listX2, listY3_1, color="r")
        self.plot(listX2, listY3_2, color="r")
        self.plot(listX2, listY3_1, -2, color="g")
        self.plot(listX2, listY3_2, -2, color="g")
        for i in range(1, 6):
            self.plot(listX, listY1, -((2*i)*2))
            self.plot(listX, listY2, -((2*i+1)*2))
            self.y_min -= 4

    def plot(self, x, y, yoffs=0, color="w"):
        lx = list(x)
        ly = list(y)
        for i in range(0, len(ly)):
            ly[i] += yoffs
        self.pyqtgraphWidget.plot(lx, ly, pen=pg.mkPen(color))

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
    
    def scroll_y(self):
        pass

    def move_line(self):
        self.infinite_line.setPos(2000)
    
    def add_functions(self):
        self.scaleIncButton.clicked.connect(lambda: self.change_x_scale(0.7))
        self.scaleDecButton.clicked.connect(lambda: self.change_x_scale(1.4))
        self.hScrollBar.valueChanged.connect(lambda: self.scroll_x())
        self.vScrollBar.valueChanged.connect(lambda: self.scroll_y())
        self.pyqtgraphWidget.scene().sigMouseClicked.connect(self.graph_click_mouse)
        self.moveLineButton.clicked.connect(lambda: self.move_line())
    
    def graph_click_mouse(self, mouseClickEvent):
        pos = mouseClickEvent.pos().x()
        shift = self.hScrollBar.minimum()
        chart_size = self.hScrollBar.maximum() - self.hScrollBar.minimum() + self.hScrollBar.pageStep()
        widget_size = self.pyqtgraphWidget.frameGeometry().width()
        scale = chart_size / widget_size
        line_pos = shift + (pos * scale)
        self.infinite_line.setPos(line_pos)
        
        # print('clicked plot 0x{:x}, event: {}'.format(id(self), mouseClickEvent))
        # print(mouseClickEvent.pos())
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
