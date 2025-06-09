from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt, QRectF


class CircularProgress(QWidget):
    def __init__(self, value=0, label="Label", color="#00F9FF", parent=None):
        super().__init__(parent)
        self.value = value
        self.label = label
        self.color = QColor(color)
        self.resize(160, 160)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def setValue(self, val):
        self.value = val
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Очистка фона прозрачным цветом
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)

        # Фон круга (серый фон прогресса)
        pen = QPen(QColor("#001c2d"), 12)
        painter.setPen(pen)
        painter.drawEllipse(10, 10, 140, 140)

        # Прогресс (цветной сектор)
        pen.setColor(self.color)
        pen.setWidth(10)
        painter.setPen(pen)
        rect = QRectF(10, 10, 140, 140)
        angle = int(360 * self.value / 100)
        painter.drawArc(rect, -90 * 16, -angle * 16)

        # Текст с процентом и названием
        painter.setPen(self.color)
        font = QFont("Arial", 9, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self.value}%\n{self.label}")