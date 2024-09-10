import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QAction, QTextEdit, QDialog, QMessageBox, QTextBrowser, QApplication
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QTimer

class MainApplication(QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle('Main Application')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout(self)

        self.username_label = QLabel(f'Welcome, {username}!')
        self.layout.addWidget(self.username_label)

        # Create a QTextBrowser widget for displaying captured screenshots
        self.screenshot_text = QTextBrowser(self)
        self.layout.addWidget(self.screenshot_text)

        # Create a button for taking screenshots
        self.screenshot_button = QPushButton('Take Screenshot', self)
        self.screenshot_button.clicked.connect(self.take_screenshot)
        self.layout.addWidget(self.screenshot_button)

        # Initialize screenshot variables
        self.screenshot_counter = 0

    def take_screenshot(self):
        screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())

        if not os.path.exists('screenshots'):
            os.mkdir('screenshots')

        screenshot_path = f"screenshots/screenshot_{self.screenshot_counter}.png"
        screenshot.save(screenshot_path)

        self.screenshot_text.append(f"Screenshot saved as: {screenshot_path}")
        self.screenshot_counter += 1


class LoginSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.user_data = {}

    def initUI(self):
        self.setWindowTitle('Login System')
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit(self)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            if username in self.user_data:
                QMessageBox.warning(self, "Registration Failed", "Username already exists. Please choose a different username.")
            else:
                self.user_data[username] = password
                self.username_input.clear()
                self.password_input.clear()
                QMessageBox.information(self, "Registration Successful", "Registration successful. You can now log in.")
        else:
            QMessageBox.warning(self, "Registration Failed", "Please enter both username and password.")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            if username in self.user_data and self.user_data[username] == password:
                self.username_input.clear()
                self.password_input.clear()
                QMessageBox.information(self, "Login Successful", f"Login successful. Welcome, {username}!")

                # Open the main application in a popup dialog
                main_app = MainApplication(username)
                main_app.exec_()
            else:
                self.username_input.clear()
                self.password_input.clear()
                QMessageBox.warning(self, "Login Failed", "Incorrect username or password. Please try again.")
        else:
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginSystem()
    window.show()
    sys.exit(app.exec_())
