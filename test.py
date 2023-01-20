from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication , QLabel , QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton, QMessageBox

app = QApplication([])
window = QWidget()
window.resize(840,590)
window.setWindowTitle('топ 1 самых жестких тестов в истории украинского интернета')
window.show()

quest = QLabel("В каком году был 1677 год?")
btn1 = QRadioButton('5285')
btn2 = QRadioButton('2018')
btn3 = QRadioButton('2026')
btn4 = QRadioButton('84572')
btn5 = QRadioButton('1')
btn6 = QRadioButton('155')
btn7 = QRadioButton('211')
btn8 = QRadioButton('89')
btn9 = QRadioButton('504')
btn10 = QRadioButton('1677')
btn11 = QRadioButton('1676')
btn12 = QRadioButton('21')

col1 = QHBoxLayout()
col2 = QHBoxLayout()
col3 = QHBoxLayout()

col1.addWidget(quest, alignment=Qt.AlignCenter)

col2.addWidget(btn1, alignment=Qt.AlignCenter)
col2.addWidget(btn2, alignment=Qt.AlignCenter)
col2.addWidget(btn3, alignment=Qt.AlignCenter)
col2.addWidget(btn4, alignment=Qt.AlignCenter)
col2.addWidget(btn5, alignment=Qt.AlignCenter)
col2.addWidget(btn6, alignment=Qt.AlignCenter)

col3.addWidget(btn7, alignment=Qt.AlignCenter)
col3.addWidget(btn8, alignment=Qt.AlignCenter)
col3.addWidget(btn9, alignment=Qt.AlignCenter)
col3.addWidget(btn10, alignment=Qt.AlignCenter)
col3.addWidget(btn11, alignment=Qt.AlignCenter)
col3.addWidget(btn12, alignment=Qt.AlignCenter)

main_line = QVBoxLayout()
main_line.addLayout(col1)
main_line.addLayout(col2)
main_line.addLayout(col3)

window.setLayout(main_line)

def win():
    winner= QMessageBox()
    winner.setText("Красавчик!\n доказал что шаришь в истории!")
    winner.exec()
def lose():
    loser = QMessageBox()
    loser.setText('Ты плохо загуглил!\n Загугли еще раз!')
    loser.exec()

btn10.clicked.connect(win)
btn1.clicked.connect(lose)
btn2.clicked.connect(lose)
btn3.clicked.connect(lose)
btn4.clicked.connect(lose)
btn5.clicked.connect(lose)
btn6.clicked.connect(lose)
btn7.clicked.connect(lose)
btn8.clicked.connect(lose)
btn9.clicked.connect(lose)
btn11.clicked.connect(lose)
btn12.clicked.connect(lose)

window.show()
app.exec_()