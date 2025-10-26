from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget,QTabWidget,QFrame, QLabel, QLineEdit, QCalendarWidget, QRadioButton, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from PyQt5.QtGui import QFont, QIcon
import sys
from datetime import datetime



class Todolist(QMainWindow):
    def __init__(self):
        super(Todolist,self).__init__()
        self.today_date = datetime.today().strftime("%Y-%m-%d")
        self.task_count = 0
        self.completed_task_count = 0
        self.today_tasks = 0
        self.tasks = []   

        uic.loadUi("todolist.ui",self)

        self.tab = self.findChild(QTabWidget,"All_task")
        self.all_frame = self.findChild(QFrame,"all_frame")
        self.today_frame = self.findChild(QFrame,"today_frame")
        self.complete_frame = self.findChild(QFrame,"frame_3")

        self.add_task_all = self.findChild(QPushButton,"pushButton")
        self.add_task_day = self.findChild(QPushButton,"pushButton_2")

        self.add_task_all.clicked.connect(self.open_add_task)
        self.add_task_day.clicked.connect(self.open_add_task_today)
    
    def open_add_task_today(self):
        self.show_add_task_window = Add_Task()
        self.show_add_task_window.show()
        self.show_add_task_window.recive_user_input.connect(self.get_day_user_input)

    def add_to_today_tab(self, name, description, date):
        y_position = 40 + (self.today_tasks * 100)
        self.today_tasks += 1

        frame_today = QFrame(self.today_frame)
        frame_today.setGeometry(50, y_position, 651, 81)
        frame_today.setStyleSheet("background-color: #EEEFE0; border-radius: 20px;")
        frame_today.show()

        task_name = QLabel(name, frame_today)
        task_name.setFont(QFont('MS Shell Dlg 2', 9))
        task_name.move(20, 10)
        task_name.show()

        task_description = QLabel(description, frame_today)
        task_description.setFont(QFont('MS Shell Dlg 2', 8))
        task_description.move(20, 30)
        task_description.show()

        task_date = QLabel(date, frame_today)
        task_date.setFont(QFont('MS Shell Dlg 2', 8))
        task_date.move(20, 55)
        task_date.show()

        complete_radio = QRadioButton(frame_today)
        complete_radio.setGeometry(430, 40, 20, 20)
        complete_radio.show()

        edit_button = QPushButton("", frame_today)
        edit_button.resize(70, 31)
        edit_button.setStyleSheet("background-color:#A7C1A8; border-radius:10px;")
        edit_button.move(470, 40)
        edit_button.setIcon(QIcon("icons8-edit-48.png"))
        edit_button.show()

        delete_button = QPushButton("", frame_today)
        delete_button.resize(70, 31)
        delete_button.setStyleSheet("background-color:#A7C1A8; border-radius:10px;")
        delete_button.move(552, 40)
        delete_button.setIcon(QIcon("icons8-trash-can-48.png"))
        delete_button.show()


    def get_day_user_input(self,name,description,date):
        if self.today_date == date:
            y_position = 40 + (self.task_count * 100)
            self.today_tasks += 1 
            self.frame_new_task = QFrame(self.today_frame)
            self.frame_new_task.setGeometry(50,y_position,651,81)
            self.frame_new_task.setStyleSheet("background-color: #EEEFE0; border-radius: 20px;")
            self.frame_new_task.show()

            self.task_name = QLabel(name,self.frame_new_task)
            self.task_name.setFont(QFont('MS Shell Dlg 2', 9))
            self.task_name.move(20, 10)
            self.task_name.show()

            self.task_description = QLabel(description,self.frame_new_task)
            self.task_description.setFont(QFont('MS Shell Dlg 2', 8))
            self.task_description.move(20, 30)
            self.task_description.show()

            self.task_date = QLabel(date ,self.frame_new_task)
            self.task_date.setFont(QFont('MS Shell Dlg 2', 8))
            self.task_date.move(20,55)
            self.task_date.show()

            self.complete_radio = QRadioButton(self.frame_new_task)
            self.complete_radio.setGeometry(430, 40, 20, 20)
            self.complete_radio.setStyleSheet("QRadioButton::indicator { width: 15px; height: 15px; }")
            self.complete_radio.show()

            self.edit_button = QPushButton("" ,self.frame_new_task)
            self.edit_button.setFont(QFont('MS Shell Dlg 2', 8))
            self.edit_button.resize(70, 31)
            self.edit_button.setStyleSheet("color: #262626 ; background-color:#A7C1A8 ; border-radius : 10px ;")
            self.edit_button.move(470, 40)
            self.edit_button.setIcon(QIcon("icons8-edit-48.png"))
            self.edit_button.show()

            self.delete_button = QPushButton("" ,self.frame_new_task)
            self.delete_button.setFont(QFont('MS Shell Dlg 2', 8))
            self.delete_button.resize(70, 31)
            self.delete_button.setStyleSheet(" color: #262626 ; background-color:#A7C1A8 ; border-radius : 10px ;")
            self.delete_button.move(552, 40)
            self.delete_button.setIcon(QIcon("icons8-trash-can-48.png"))
            self.delete_button.show()

            task_data = {
                'frame': self.frame_new_task,
                'name': self.task_name,
                'description': self.task_description,
                'date': self.task_date,
                'complete_radio': self.complete_radio,
                'edit_button': self.edit_button,
                'delete_button': self.delete_button
            }

            self.tasks.append(task_data)

            self.complete_radio.toggled.connect(lambda : self.complete_task_today(task_data,name,description,date))
            self.edit_button.clicked.connect(lambda: self.edit_task_today(task_data))
            self.delete_button.clicked.connect(lambda: self.delete_task_today(task_data))

            self.get_user_input(name, description, date, skip_today=True)

        else:
            self.get_user_input(name,description,date)

    def complete_task_today(self,task_data,name,description,date):
        if hasattr(self, 'complete_win') and self.complete_win.isVisible():
            self.complete_win.add_task(
                task_data['name'].text(),
                task_data['description'].text(),
                task_data['date'].text()
            )

        self.delete_task(task_data)
        y_position = 20 + (self.task_count * 100)
        self.completed_task_count += 1 
        self.frame_new_task = QFrame(self.complete_frame)
        self.frame_new_task.setGeometry(50,y_position,651,81)
        self.frame_new_task.setStyleSheet("background-color: #EEEFE0; border-radius: 20px;")
        self.frame_new_task.show()

        self.task_name = QLabel(name,   self.frame_new_task)
        self.task_name.setFont(QFont('MS Shell Dlg 2', 9))
        self.task_name.move(20, 10)
        self.task_name.show()

        self.task_description = QLabel(description,  self.frame_new_task)
        self.task_description.setFont(QFont('MS Shell Dlg 2', 8))
        self.task_description.move(20, 30)
        self.task_description.show()

        self.task_date = QLabel(date,  self.frame_new_task)
        self.task_date.setFont(QFont('MS Shell Dlg 2', 8))
        self.task_date.move(20,55)
        self.task_date.show()

        self.delete_button = QPushButton("" ,self.frame_new_task)
        self.delete_button.setFont(QFont('MS Shell Dlg 2', 8))
        self.delete_button.resize(70, 31)
        self.delete_button.setStyleSheet(" color: #262626 ; background-color:#A7C1A8 ; border-radius : 10px ;")
        self.delete_button.move(552, 40)
        self.delete_button.setIcon(QIcon("icons8-trash-can-48.png"))
        self.delete_button.show()
            

    def edit_task_today(self,task_data):
        task_data['frame'].deleteLater()
        self.tasks.remove(task_data)
        self.today_tasks -= 1
        self.open_add_task_today()

    def delete_task_today(self,task_data):
        task_data['frame'].deleteLater()
        self.tasks.remove(task_data)
        self.today_tasks -= 1


    def open_add_task(self):
        self.show_add_task_window = Add_Task()
        self.show_add_task_window.show()
        self.show_add_task_window.recive_user_input.connect(self.get_user_input)

    def get_user_input(self,name,description,date,skip_today=False):
        y_position = 40 + (self.task_count * 100)
        self.task_count += 1 
        self.frame_new_task = QFrame(self.all_frame)
        self.frame_new_task.setGeometry(50,y_position,651,81)
        self.frame_new_task.setStyleSheet("background-color: #EEEFE0; border-radius: 20px;")
        self.frame_new_task.show()

        self.task_name = QLabel(name,   self.frame_new_task)
        self.task_name.setFont(QFont('MS Shell Dlg 2', 9))
        self.task_name.move(20, 10)
        self.task_name.show()

        self.task_description = QLabel(description,  self.frame_new_task)
        self.task_description.setFont(QFont('MS Shell Dlg 2', 8))
        self.task_description.move(20, 30)
        self.task_description.show()

        self.task_date = QLabel(date ,  self.frame_new_task)
        self.task_date.setFont(QFont('MS Shell Dlg 2', 8))
        self.task_date.move(20,55)
        self.task_date.show()

        self.complete_radio = QRadioButton(self.frame_new_task)
        self.complete_radio.setGeometry(430, 40, 20, 20)
        self.complete_radio.setStyleSheet("QRadioButton::indicator { width: 15px; height: 15px; }")
        self.complete_radio.show()

        self.edit_button = QPushButton("" ,self.frame_new_task)
        self.edit_button.setFont(QFont('MS Shell Dlg 2', 8))
        self.edit_button.resize(70, 31)
        self.edit_button.setStyleSheet("color: #262626 ; background-color:#A7C1A8 ; border-radius : 10px ;")
        self.edit_button.move(470, 40)
        self.edit_button.setIcon(QIcon("icons8-edit-48.png"))
        self.edit_button.show()

        self.delete_button = QPushButton("" ,self.frame_new_task)
        self.delete_button.setFont(QFont('MS Shell Dlg 2', 8))
        self.delete_button.resize(70, 31)
        self.delete_button.setStyleSheet(" color: #262626 ; background-color:#A7C1A8 ; border-radius : 10px ;")
        self.delete_button.move(552, 40)
        self.delete_button.setIcon(QIcon("icons8-trash-can-48.png"))
        self.delete_button.show()

        task_data = {
            'frame': self.frame_new_task,
            'name': self.task_name,
            'description': self.task_description,
            'date': self.task_date,
            'complete_radio': self.complete_radio,
            'edit_button': self.edit_button,
            'delete_button': self.delete_button
        }

        self.tasks.append(task_data)
        print(self.tasks)
        print(task_data)

        self.complete_radio.toggled.connect(lambda : self.complete_task(task_data,name,description,date))
        self.edit_button.clicked.connect(lambda: self.edit_task(task_data))
        self.delete_button.clicked.connect(lambda: self.delete_task(task_data))

        if (not skip_today) and (self.today_date == date):
            self.add_to_today_tab(name, description, date)

    def complete_task(self,task_data,name,description,date):
        
        if hasattr(self, 'complete_win') and self.complete_win.isVisible():
            self.complete_win.add_task(
                task_data['name'].text(),
                task_data['description'].text(),
                task_data['date'].text()
            )

        self.delete_task(task_data)
        y_position = 20 + (self.task_count * 100)
        self.completed_task_count += 1 
        self.frame_new_task = QFrame(self.complete_frame)
        self.frame_new_task.setGeometry(50,y_position,651,81)
        self.frame_new_task.setStyleSheet("background-color: #EEEFE0; border-radius: 20px;")
        self.frame_new_task.show()

        self.task_name = QLabel(name,   self.frame_new_task)
        self.task_name.setFont(QFont('MS Shell Dlg 2', 9))
        self.task_name.move(20, 10)
        self.task_name.show()

        self.task_description = QLabel(description,  self.frame_new_task)
        self.task_description.setFont(QFont('MS Shell Dlg 2', 8))
        self.task_description.move(20, 30)
        self.task_description.show()

        self.task_date = QLabel(date,  self.frame_new_task)
        self.task_date.setFont(QFont('MS Shell Dlg 2', 8))
        self.task_date.move(20,55)
        self.task_date.show()

        self.delete_button = QPushButton("" ,self.frame_new_task)
        self.delete_button.setFont(QFont('MS Shell Dlg 2', 8))
        self.delete_button.resize(70, 31)
        self.delete_button.setStyleSheet(" color: #262626 ; background-color:#A7C1A8 ; border-radius : 10px ;")
        self.delete_button.move(552, 40)
        self.delete_button.setIcon(QIcon("icons8-trash-can-48.png"))
        self.delete_button.show()
        

    def edit_task(self,task_data):
        task_data['frame'].deleteLater()
        self.tasks.remove(task_data)
        self.task_count -= 1
        self.open_add_task()

    def delete_task(self,task_data):
        task_data['frame'].deleteLater()
        self.tasks.remove(task_data)
        self.task_count -= 1

class Add_Task(QMainWindow):
    recive_user_input = pyqtSignal(str,str,str)

    def __init__(self):
        super(Add_Task,self).__init__()

        # Load Ui File
        uic.loadUi("Add_Task_file.ui",self)

        # Define All Widgets
        self.frame = self.findChild(QFrame,"frame")
        
        self.AddTask_Button = self.findChild(QPushButton,"pushButton_2")
        self.Cancel_Button = self.findChild(QPushButton,"Cancel_Button")
        self.Date_Button = self.findChild(QPushButton,"Delete_Button")
        
        self.Task_name = self.findChild(QLineEdit,"Task_name") 
        self.Description = self.findChild(QLineEdit,"DEscription") 

        self.date_label = None

        self.AddTask_Button.clicked.connect(self.send_user_input)
        self.Date_Button.clicked.connect(self.set_date)
        self.Cancel_Button.clicked.connect(self.cancel)
    

    def send_user_input(self):
        task_name = self.Task_name.text()
        task_description = self.Description.text()
        get_date = self.date_label.text() if self.date_label else datetime.today().strftime("%Y-%m-%d")
        self.recive_user_input.emit(task_name, task_description,get_date)
        self.hide()
            
    def set_date(self):
        self.calendar_window = Calender()  
        self.calendar_window.show()
        self.calendar_window.calender.selectionChanged.connect(self.grab_all)

    def grab_all(self):
        dateselection = self.calendar_window.calender.selectedDate()
        self.date_label = QLabel(str(dateselection.toString("yyyy-MM-dd")),self.frame)
        self.calendar_window.hide()
        self.date_label.setGeometry(30,90,101,21)
        self.date_label.show()

        return dateselection.toString("yyyy-MM-dd")
    
    def cancel(self):
        self.hide()

class Calender(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GUI Calendar")
        self.setGeometry(100, 100, 400, 300)

        self.calender = QCalendarWidget(self)
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
                background-color: #D1D8BE;
            }
            QCalendarWidget QToolButton {
                color: black;
                background-color: #D1D8BE;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #D1D8BE;
            }
        """)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Todolist()
    window.show()

    sys.exit(app.exec_())

