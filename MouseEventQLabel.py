
from PyQt5 import QtWidgets
from util import log

class MyQLabel (QtWidgets.QLabel):
    
    boundary = None
    
    pressed_x = 0
    pressed_y = 0

    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
        #self.setText('Lorem Ipsum')
        #print (parent.geometry())
        self.boundary = parent.geometry()

    def mouseReleaseEvent(self, event):
        log (f'Label clicked! ({event.pos().x()},{event.pos().y()})')

    def mousePressEvent (self, event):
        log (f'Label Pressed! ({event.pos().x()},{event.pos().y()}) Geo: ({self.x()},{self.y()})')
        self.pressed_x = event.pos().x()
        self.pressed_y = event.pos().y()

    def mouseMoveEvent (self, event):
        log (f'Label Moved !({event.pos().x()},{event.pos().y()})')
        delta_x = event.pos().x() - self.pressed_x
        delta_y = event.pos().y() - self.pressed_y

        updated_x = self.x()+delta_x
        updated_y = self.y()+delta_y

        log (f'Label Updated To !({updated_x},{updated_y})')
        
        if updated_x >= self.boundary.x() and updated_x <= (self.boundary.x() + self.boundary.width()) - self.fontMetrics().boundingRect(self.text()).width() \
             and updated_y >= self.boundary.y() + 22 and updated_y <= (self.boundary.y() + self.boundary.height())  :
            self.move(updated_x, updated_y)

    def setBoundary (self, rect):
        self.boundary = rect

    def getBoundary (self):
        return self.boundary

    