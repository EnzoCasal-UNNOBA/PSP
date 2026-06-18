from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QTimeEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


class ActivitiesPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # --- Formulario arriba ---
        form_layout = QFormLayout()

        self.date_field = QDateEdit()
        self.date_field.setCalendarPopup(True)

        self.start_time_field = QTimeEdit()
        self.end_time_field = QTimeEdit()

        self.interruptions_field = QLineEdit()

        self.job_field = QComboBox()
        self.job_field.addItem("Seleccionar Job...")  # placeholder

        self.description_field = QTextEdit()

        form_layout.addRow("Fecha:", self.date_field)
        form_layout.addRow("Inicio:", self.start_time_field)
        form_layout.addRow("Fin:", self.end_time_field)
        form_layout.addRow("Interrupciones:", self.interruptions_field)
        form_layout.addRow("Job:", self.job_field)
        form_layout.addRow("Descripción:", self.description_field)

        self.save_button = QPushButton("Guardar actividad")

        # Layout del formulario + botón
        form_container = QVBoxLayout()
        form_container.addLayout(form_layout)
        form_container.addWidget(self.save_button)

        main_layout.addLayout(form_container)

        # --- Tabla abajo ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Inicio", "Fin", "Job", "Descripción"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ejemplo de fila placeholder
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem("15/06/2026"))
        self.table.setItem(0, 1, QTableWidgetItem("08:00"))
        self.table.setItem(0, 2, QTableWidgetItem("10:00"))
        self.table.setItem(0, 3, QTableWidgetItem("Login"))
        self.table.setItem(0, 4, QTableWidgetItem("Implementación inicial"))

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
