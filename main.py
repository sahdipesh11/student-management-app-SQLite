from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Add menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add sub-item (action) to the file menu item
        add_student_action = QAction("Add student", self)
        add_student_action.triggered.connect(self.insert) # Call insert method
        file_menu_item.addAction(add_student_action)

        # Add sub-item (action) to the help menu item
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Add a table widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table) # Specify table as central widget.

    def load_date(self):
        # Create a connection to the database and read data from student table.
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")

        # Populate table with data
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # QVBoxLayout creates widget with vertical input boxes.
        layout = QVBoxLayout()

        # Add student name widget.
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combobox of courses.
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile number widget.
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student) # Call add_student method.
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        # Create name, course and mobile variables that takes the input
        # provided in the dialog box
        name = self.student_name.text()
        # Give the choice that user made in combobox.
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) "
                       "VALUES (?, ?,  ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_date()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_date()
sys.exit(app.exec())