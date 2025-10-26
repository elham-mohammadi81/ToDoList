from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QFrame,QLineEdit,QCalendarWidget,QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QBrush, QColor , QTextCharFormat
from PyQt5 import uic
import sys 
# from All_file import All_Task


class Add_Task(QMainWindow):

    recive_user_input = pyqtSignal(str,str,str)

    def __init__(self):
        super(Add_Task,self).__init__()

        # Load Ui File
        uic.loadUi("G:/Python/Projects/ToDoList/Add_Task_file.ui",self)

        # Define All Widgets
        self.frame = self.findChild(QFrame,"frame")
        
        self.AddTask_Button = self.findChild(QPushButton,"pushButton_2")
        self.Cancel_Button = self.findChild(QPushButton,"Cancel_Button")
        self.Date_Button = self.findChild(QPushButton,"Delete_Button")
        
        self.Task_name = self.findChild(QLineEdit,"Task_name") 
        self.Description = self.findChild(QLineEdit,"DEscription") 

        self.AddTask_Button.clicked.connect(self.send_user_input)
        self.Date_Button.clicked.connect(self.set_date)
        self.Cancel_Button.clicked.connect(self.cancel)


    def send_user_input(self):
        task_name = self.Task_name.text()
        task_description = self.Description.text()
        get_date = self.grab_all()
        self.recive_user_input.emit(task_name, task_description,get_date)
        self.close()

    def set_date(self):
        self.calendar_window = Calender()  
        self.calendar_window.show()
        self.calendar_window.calender.selectionChanged.connect(self.grab_all)

    def grab_all(self):
        dateselection = self.calendar_window.calender.selectedDate()
        self.date_label = QLabel(str(dateselection.toString()),self.frame)
        self.calendar_window.hide()
        self.date_label.setGeometry(30,90,101,21)
        self.date_label.show()
        return str(dateselection.toString())
    def cancel(self):
        self.hide()




class Calender(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GUI Calendar")
        self.setGeometry(100, 100, 400, 300)

        self.calender = QCalendarWidget(self)
        self.calender.setGeometry(10, 10, 380, 280)
        self.calender.setGeometry(10, 10, 380, 280)

        self.calender.setStyleSheet("""
    QCalendarWidget {
        background-color: #D1D8BE;
        border-radius: 20px;
    }

    QCalendarWidget QAbstractItemView:enabled:item:selected {
        background-color: #D1D8BE;
        color: black;
    }

    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #D1D8BE;   /* رنگ نوار بالای تقویم */
    }

    QCalendarWidget QToolButton {
        color: black;
        background-color: #D1D8BE;   /* رنگ دکمه‌های ماه قبل/بعد */
        border-radius: 8px;
    }

    QCalendarWidget QToolButton:hover {
        background-color: #D1D8BE;   /* رنگ دکمه‌ها هنگام hover */
    }
""")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Add_Task()
    window.show()
    sys.exit(app.exec_())