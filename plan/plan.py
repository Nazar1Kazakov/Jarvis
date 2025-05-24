from PyQt5 import QtWidgets, QtGui, QtCore
from qt_material import apply_stylesheet

DAYS = [
    "Понедельник", "Вторник", "Среда",
    "Четверг", "Пятница", "Суббота", "Воскресенье"
]

SCHEDULE = {
 "Понедельник": [
        ("05:30", "Подъём, заправка кровати"),
        ("05:40", "Душ, умывание, гигиена"),
        ("06:00", "Завтрак"),
        ("06:20", "Зарядка / медитация / планирование"),
        ("06:40", "Программирование / самообучение"),
        ("08:00", "Перекус / отдых"),
        ("08:15", "Сборы, выход"),
        ("08:30", "Дорога в школу"),
        ("09:00", "Учёба"),
        ("16:00", "Дорога домой"),
        ("16:30", "Обед"),
        ("17:00", "Домашка по школьным предметам"),
        ("18:00", "Отдых, YouTube, игры"),
        ("18:30", "Работа над проектом"),
        ("19:30", "Подготовка к тренировке"),
        ("20:00", "Тренировка"),
        ("21:00", "Душ"),
        ("21:20", "Ужин"),
        ("21:40", "Подготовка ко сну")
    ],
    "Вторник": [
        ("05:30", "Подъём"),
        ("05:40", "Гигиена"),
        ("06:00", "Завтрак"),
        ("06:20", "Чтение или разминка"),
        ("06:40", "Программирование"),
        ("08:00", "Сборы"),
        ("08:30", "Школа"),
        ("16:00", "Обед"),
        ("17:00", "Домашка"),
        ("18:00", "Свободное время"),
        ("18:30", "Учебный проект"),
        ("20:00", "Спорт"),
        ("21:00", "Ужин и отдых")
    ],
    "Среда": [
        ("05:30", "Подъём"),
        ("05:40", "Душ"),
        ("06:00", "Завтрак"),
        ("06:30", "Учёба или проект"),
        ("08:30", "Школа"),
        ("16:00", "Домой и обед"),
        ("17:00", "Домашка"),
        ("18:30", "Кодинг"),
        ("20:00", "Спорт"),
        ("21:00", "Ужин")
    ],
    "Четверг": [
        ("05:30", "Подъём"),
        ("05:45", "Гигиена"),
        ("06:00", "Завтрак"),
        ("06:30", "Повторение изученного"),
        ("08:30", "Школа"),
        ("16:00", "Обед"),
        ("17:00", "Домашка"),
        ("18:00", "Проект или хобби"),
        ("20:00", "Тренировка"),
        ("21:00", "Душ и сон")
    ],
    "Пятница": [
        ("05:30", "Подъём"),
        ("05:45", "Гигиена"),
        ("06:00", "Завтрак"),
        ("06:30", "Учёба"),
        ("08:30", "Школа"),
        ("16:00", "Обед"),
        ("17:00", "Домашка"),
        ("18:00", "Свободное время"),
        ("20:00", "Спорт"),
        ("21:00", "Фильм / отдых")
    ],
    "Суббота": [
        ("08:00", "Подъём"),
        ("08:15", "Завтрак"),
        ("08:45", "Проекты"),
        ("11:00", "Прогулка"),
        ("13:00", "Обед"),
        ("14:00", "Учёба или кодинг"),
        ("17:00", "Игры"),
        ("19:00", "Ужин"),
        ("20:00", "Отдых")
    ],
    "Воскресенье": [
        ("08:30", "Подъём"),
        ("09:00", "Завтрак"),
        ("10:00", "Лёгкие дела / творчество"),
        ("12:00", "Прогулка"),
        ("14:00", "Обед"),
        ("15:00", "Чтение или сериал"),
        ("17:00", "Подготовка к новой неделе"),
        ("19:00", "Ужин"),
        ("20:00", "Отдых и сон")
    ]
}

class ScheduleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS – Расписание дня")
        self.setGeometry(100, 100, 800, 600)

        # ✅ Устанавливаем иконку для панели задач и окна
        self.setWindowIcon(QtGui.QIcon("favicon.ico"))

        self.day_index = 0
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.day_label = QtWidgets.QLabel()
        self.day_label.setAlignment(QtCore.Qt.AlignCenter)
        self.day_label.setStyleSheet("font-size: 28px; color: #00FFF7;")

        self.schedule_list = QtWidgets.QListWidget()
        self.schedule_list.setStyleSheet(
            "font-size: 18px; color: white; background-color: #101010; border: none;")

        self.prev_button = QtWidgets.QPushButton("←")
        self.next_button = QtWidgets.QPushButton("→")
        for btn in (self.prev_button, self.next_button):
            btn.setFixedSize(50, 50)
            btn.setStyleSheet("border-radius: 25px; font-size: 24px; background-color: #00FFF7; color: black;")

        self.nav_layout = QtWidgets.QHBoxLayout()
        self.nav_layout.addWidget(self.prev_button)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.next_button)

        self.layout.addWidget(self.day_label)
        self.layout.addWidget(self.schedule_list)
        self.layout.addLayout(self.nav_layout)

        self.prev_button.clicked.connect(self.prev_day)
        self.next_button.clicked.connect(self.next_day)

        self.update_schedule()

    def update_schedule(self):
        day = DAYS[self.day_index]
        self.day_label.setText(day)
        self.schedule_list.clear()
        for time, activity in SCHEDULE.get(day, []):
            self.schedule_list.addItem(f"{time} — {activity}")

    def prev_day(self):
        self.day_index = (self.day_index - 1) % len(DAYS)
        self.update_schedule()

    def next_day(self):
        self.day_index = (self.day_index + 1) % len(DAYS)
        self.update_schedule()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # 🧠 Не забываем установить иконку для QApplication (для панели задач!)
    app.setWindowIcon(QtGui.QIcon("favicon.ico"))

    apply_stylesheet(app, theme="dark_teal.xml")
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec_())
