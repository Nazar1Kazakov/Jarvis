from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt


class CircularLabel(QWidget):
    def __init__(self, text, color="#00F9FF", parent=None):
        super().__init__(parent)
        self.text = text
        self.color = QColor(color)
        self.setFixedSize(160, 160)  # Размер совпадает с CircularProgress

    def setText(self, text):
        self.text = text
        self.update()  # Перерисовать виджет

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Рисуем круг (контур)
        pen = QPen(self.color, 5)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(10, 10, 140, 140)

        # Рисуем текст по центру
        painter.setPen(self.color)
        font = QFont("Arial", 10, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text)
