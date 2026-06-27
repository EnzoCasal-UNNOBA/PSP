from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QDateEdit,
    QTimeEdit,
    QTextEdit,
    QComboBox,
    QSpinBox,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
    QAbstractItemView
)


class ActivitiesPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        # ===================================================
        # TÍTULO
        # ===================================================
        title = QLabel("Daily Log")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # ===================================================
        # FORMULARIO
        # ===================================================
        form_group = QGroupBox("Registrar actividad")
        form = QFormLayout()

        self.date_field = QDateEdit()
        self.date_field.setCalendarPopup(True)
        self.date_field.setDate(QDate.currentDate())
        self.date_field.setDisplayFormat("dd/MM/yyyy")

        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setTime(QTime.currentTime())

        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setTime(QTime.currentTime().addSecs(3600))

        self.job_combo = QComboBox()
        self.job_combo.addItem("Seleccionar Job...")

        self.interruptions = QSpinBox()
        self.interruptions.setRange(0, 999)

        self.description = QTextEdit()
        self.description.setPlaceholderText("Descripción breve...")
        self.description.setFixedHeight(55)
        self.description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        form.addRow("Fecha", self.date_field)
        form.addRow("Hora inicio", self.start_time)
        form.addRow("Hora fin", self.end_time)
        form.addRow("Job", self.job_combo)
        form.addRow("Interrupciones", self.interruptions)
        form.addRow("Descripción", self.description)

        self.save_button = QPushButton("Guardar actividad")
        self.save_button.setObjectName("primaryButton")
        form.addRow(self.save_button)

        form_group.setLayout(form)
        main_layout.addWidget(form_group)

        # ===================================================
        # TABLA
        # ===================================================
        table_group = QGroupBox("Actividades del día")
        table_layout = QVBoxLayout()

        crud = QHBoxLayout()
        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Eliminar")
        self.refresh_button = QPushButton("Actualizar")
        crud.addWidget(self.edit_button)
        crud.addWidget(self.delete_button)
        crud.addWidget(self.refresh_button)
        crud.addStretch()
        table_layout.addLayout(crud)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Inicio", "Fin", "Int.", "Job", "Descripción"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setMinimumHeight(280)

        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)
