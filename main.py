from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem
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


app = QApplication(sys.argv)
age_calculator = MainWindow()
age_calculator.show()
age_calculator.load_date()
sys.exit(app.exec())