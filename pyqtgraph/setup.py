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
        self.plot(listX, listY1)
        self.plot(listX, listY2, 2)

    def plot(self, x, y, yoffs=0):
        for i in range(0, len(y)):
            y[i] += yoffs
        self.pyqtgraphWidget.plot(x, y)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
