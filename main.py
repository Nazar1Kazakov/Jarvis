import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, pyqtProperty, QSize
from PyQt6.QtGui import QPainter, QPen, QColor
from temp_monitor import get_cpu_temp, get_cpu_load, get_gpu_temp_and_load, get_ram_usage
from circular_widget import CircularLabel
from circular_progress import CircularProgress
from voice_input import listen_voice


# Константы для стилей
NEON_BLUE = "#00F9FF"
ALERT_RED = "#FF005C"
BACKGROUND_COLOR = "#000b16"
FONT_FAMILY = "Arial"
BUTTON_RADIUS = 125
ANIMATION_DURATION = 900


class JarvisAnimation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(500, 500)

        self._start_angle_inner = 0 * 16
        self._span_angle_inner = 270 * 16

        self._start_angle_outer = 0 * 16
        self._span_angle_outer = 270 * 16

        self.button = QPushButton("JARVIS", self)
        self.button.clicked.connect(parent.on_button_clicked if parent else self.animate_dummy)
        self.button.setFixedSize(BUTTON_RADIUS * 2, BUTTON_RADIUS * 2)
        self.button.move(
            (self.width() - self.button.width()) // 2,
            (self.height() - self.button.height()) // 2
        )
        self.button.setStyleSheet(f"""
            QPushButton {{
                border-radius: {BUTTON_RADIUS}px;
                border: 4px solid {NEON_BLUE};
                color: {NEON_BLUE};
                font-size: 24px;
                font-family: {FONT_FAMILY};
                font-weight: bold;
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: {NEON_BLUE};
                color: black;
            }}
        """)

    def get_start_angle_inner(self): return self._start_angle_inner
    def set_start_angle_inner(self, val):
        self._start_angle_inner = val
        self.update()
    start_angle_inner = pyqtProperty(int, get_start_angle_inner, set_start_angle_inner)

    def get_span_angle_inner(self): return self._span_angle_inner
    def set_span_angle_inner(self, val):
        self._span_angle_inner = val
        self.update()
    span_angle_inner = pyqtProperty(int, get_span_angle_inner, set_span_angle_inner)

    def get_start_angle_outer(self): return self._start_angle_outer
    def set_start_angle_outer(self, val):
        self._start_angle_outer = val
        self.update()
    start_angle_outer = pyqtProperty(int, get_start_angle_outer, set_start_angle_outer)

    def get_span_angle_outer(self): return self._span_angle_outer
    def set_span_angle_outer(self, val):
        self._span_angle_outer = val
        self.update()
    span_angle_outer = pyqtProperty(int, get_span_angle_outer, set_span_angle_outer)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_rect = self.button.geometry()

        # Тень для внешней дуги
        shadow_color_outer = QColor(0, 249, 255, 80)
        pen_shadow_outer = QPen(shadow_color_outer, 14, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_shadow_outer)
        outer_rect_shadow = center_rect.adjusted(-43, -43, 43, 43)
        painter.drawArc(outer_rect_shadow.translated(3, 3), self._start_angle_outer, self._span_angle_outer)

        # Основная внешняя дуга
        pen_outer = QPen(QColor(NEON_BLUE), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_outer)
        outer_rect = center_rect.adjusted(-40, -40, 40, 40)
        painter.drawArc(outer_rect, self._start_angle_outer, self._span_angle_outer)

        # Тень для внутренней дуги
        shadow_color_inner = QColor(0, 249, 255, 60)
        pen_shadow_inner = QPen(shadow_color_inner, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_shadow_inner)
        inner_rect_shadow = center_rect.adjusted(-23, -23, 23, 23)
        painter.drawArc(inner_rect_shadow.translated(2, 2), self._start_angle_inner, self._span_angle_inner)

        # Основная внутренняя дуга
        pen_inner = QPen(QColor(NEON_BLUE), 5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_inner)
        inner_rect = center_rect.adjusted(-20, -20, 20, 20)
        painter.drawArc(inner_rect, self._start_angle_inner, self._span_angle_inner)


class StatsThread(QThread):
    stats_updated = pyqtSignal(float, float, float)

    def run(self):
        while True:
            _, ram_percent = get_ram_usage()
            cpu_load = get_cpu_load()
            _, gpu_load = get_gpu_temp_and_load()

            self.stats_updated.emit(
                ram_percent if ram_percent is not None else 0,
                cpu_load if cpu_load is not None else 0,
                gpu_load if gpu_load is not None else 0
            )
            self.msleep(1000)


class WeatherThread(QThread):
    weather_updated = pyqtSignal(str)

    def run(self):
        while True:
            temp = random.randint(60, 80)
            conditions = random.choice(["☀️", "☁️", "🌧️", "⛅"])
            weather_text = f"{conditions}\n{temp}°F"
            self.weather_updated.emit(weather_text)
            self.msleep(60000)


class VoiceInputThread(QThread):
    def run(self):
        listen_voice()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.stats_thread = StatsThread()
        self.stats_thread.stats_updated.connect(self.on_stats_updated)
        self.stats_thread.start()

        self.weather_thread = WeatherThread()
        self.weather_thread.weather_updated.connect(self.on_weather_updated)
        self.weather_thread.start()

        self.voice_thread = None  # Поток для голосового ввода

        self.start_pulse_animation()
        self.add_neon_effect(self.jarvis_animation.button)

        self.anim_start_inner = QPropertyAnimation(self.jarvis_animation, b"start_angle_inner")
        self.anim_span_inner = QPropertyAnimation(self.jarvis_animation, b"span_angle_inner")
        self.anim_start_outer = QPropertyAnimation(self.jarvis_animation, b"start_angle_outer")
        self.anim_span_outer = QPropertyAnimation(self.jarvis_animation, b"span_angle_outer")

        self.angle_timer = QTimer(self)
        self.angle_timer.timeout.connect(self.animate_arcs)
        self.angle_timer.start(1000)

        self.animate_arcs()

    def initUI(self):
        self.setGeometry(400, 100, 1000, 700)
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")
        self.setWindowTitle("Jarvis")

        self.weather_circle = CircularLabel("☁️\n72°F", NEON_BLUE)
        self.weather_circle.setFixedSize(160, 160)

        weather_layout = QVBoxLayout()
        weather_layout.addWidget(self.weather_circle)
        weather_layout.addStretch()
        weather_container = QWidget()
        weather_container.setLayout(weather_layout)

        self.ram = CircularProgress(0, "RAM", NEON_BLUE)
        self.cpu = CircularProgress(0, "CPU", NEON_BLUE)
        self.gpu = CircularProgress(0, "GPU", ALERT_RED)

        for w in [self.ram, self.cpu, self.gpu]:
            w.setFixedSize(160, 160)

        indicators_layout = QVBoxLayout()
        indicators_layout.addWidget(self.ram)
        indicators_layout.addSpacing(20)
        indicators_layout.addWidget(self.cpu)
        indicators_layout.addSpacing(20)
        indicators_layout.addWidget(self.gpu)
        indicators_layout.addStretch()
        indicators_container = QWidget()
        indicators_container.setLayout(indicators_layout)

        self.jarvis_animation = JarvisAnimation(parent=self)

        center_layout = QHBoxLayout()
        center_layout.addWidget(weather_container)
        center_layout.addStretch()
        center_layout.addWidget(self.jarvis_animation)
        center_layout.addStretch()
        center_layout.addWidget(indicators_container)

        buttons_layout = QHBoxLayout()
        for name in ["Home", "System", "Network", "Weather", "Music", "Commands"]:
            btn = QPushButton(name)
            btn.setStyleSheet(f"""
                QPushButton {{
                    color: {NEON_BLUE};
                    background-color: transparent;
                    border: 1px solid {NEON_BLUE};
                    border-radius: 10px;
                    padding: 6px 12px;
                    font-family: {FONT_FAMILY};
                }}
                QPushButton:hover {{
                    background-color: {NEON_BLUE};
                    color: black;
                }}
            """)
            self.add_neon_effect(btn)
            buttons_layout.addWidget(btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(center_layout)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def on_stats_updated(self, ram_percent, cpu_load, gpu_load):
        self.ram.setValue(ram_percent)
        self.cpu.setValue(cpu_load)
        self.gpu.setValue(gpu_load)

    def on_weather_updated(self, text):
        self.weather_circle.setText(text)

    def start_pulse_animation(self):
        button = self.jarvis_animation.button
        center = button.geometry().center()

        self.anim = QPropertyAnimation(button, b"size")
        self.anim.setDuration(ANIMATION_DURATION)
        self.anim.setStartValue(button.size())
        self.anim.setKeyValueAt(0.5, button.size() + QSize(20, 20))
        self.anim.setEndValue(button.size())
        self.anim.setLoopCount(-1)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        def on_value_changed():
            new_rect = button.geometry()
            new_center = new_rect.center()
            dx = center.x() - new_center.x()
            dy = center.y() - new_center.y()
            button.move(button.x() + dx, button.y() + dy)

        self.anim.valueChanged.connect(on_value_changed)
        self.anim.start()

    def add_neon_effect(self, widget):
        effect = QGraphicsDropShadowEffect()
        effect.setColor(QColor(0, 249, 255))
        effect.setBlurRadius(20)
        effect.setOffset(0)
        widget.setGraphicsEffect(effect)

    def animate_arcs(self):
        self.anim_start_inner.stop()
        self.anim_span_inner.stop()
        self.anim_start_outer.stop()
        self.anim_span_outer.stop()

        new_start_inner = random.randint(0, 360) * 16
        new_span_inner = random.randint(200, 300) * 16
        new_start_outer = random.randint(0, 360) * 16
        new_span_outer = random.randint(200, 300) * 16

        self.anim_start_inner.setStartValue(self.jarvis_animation.start_angle_inner)
        self.anim_start_inner.setEndValue(new_start_inner)
        self.anim_start_inner.setDuration(ANIMATION_DURATION)

        self.anim_span_inner.setStartValue(self.jarvis_animation.span_angle_inner)
        self.anim_span_inner.setEndValue(new_span_inner)
        self.anim_span_inner.setDuration(ANIMATION_DURATION)

        self.anim_start_outer.setStartValue(self.jarvis_animation.start_angle_outer)
        self.anim_start_outer.setEndValue(new_start_outer)
        self.anim_start_outer.setDuration(ANIMATION_DURATION)

        self.anim_span_outer.setStartValue(self.jarvis_animation.span_angle_outer)
        self.anim_span_outer.setEndValue(new_span_outer)
        self.anim_span_outer.setDuration(ANIMATION_DURATION)

        self.anim_start_inner.start()
        self.anim_span_inner.start()
        self.anim_start_outer.start()
        self.anim_span_outer.start()

    def on_button_clicked(self):
        self.animate_arcs()
        if self.voice_thread is None or not self.voice_thread.isRunning():
            self.voice_thread = VoiceInputThread()
            self.voice_thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
