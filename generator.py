from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication , QLabel , QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton
from random import randint 

app = QApplication([])
window = QWidget()
window.resize(540,290)
window.setWindowTitle('крутой рандомайзер вообще класс урааа урааааа')
window.show()

winner = QLabel("*подкупаем рандомайзер* ")
rand = QLabel("?")
btn = QPushButton("не нажимай пожалуйста")
col = QVBoxLayout()

col.addWidget(winner, alignment=Qt.AlignCenter)
col.addWidget(rand, alignment=Qt.AlignCenter)
col.addWidget(btn, alignment=Qt.AlignCenter)
window.setLayout(col)

def show_winner():
    num = randint(1,10)
    rand.setText(str(num))
    winner.setText('красавчик : ')

btn.clicked.connect(show_winner)
app.exec_()