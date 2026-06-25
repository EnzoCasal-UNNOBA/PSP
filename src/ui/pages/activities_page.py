from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QDateEdit,
    QTimeEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
    QSpinBox,
    QAbstractItemView,
    QGroupBox
)


class ActivitiesPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # =====================================
        # Título
        # =====================================
        title = QLabel("Daily Log")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # =====================================
        # Formulario dentro de un GroupBox
        # =====================================
        form_group = QGroupBox("Registrar actividad")
        form_layout = QFormLayout()

        self.date_field = QDateEdit()
        self.date_field.setCalendarPopup(True)
        self.date_field.setDisplayFormat("dd/MM/yyyy")
        self.date_field.setDate(QDate.currentDate())

        self.start_time_field = QTimeEdit()
        self.start_time_field.setDisplayFormat("HH:mm")
        self.start_time_field.setTime(QTime.currentTime())

        self.end_time_field = QTimeEdit()
        self.end_time_field.setDisplayFormat("HH:mm")
        self.end_time_field.setTime(QTime.currentTime().addSecs(3600))

        self.job_field = QComboBox()
        self.job_field.addItem("Seleccionar Job...")
        self.job_field.setCurrentIndex(0)

        self.interruptions_field = QSpinBox()
        self.interruptions_field.setRange(0, 999)

        self.description_field = QTextEdit()
        self.description_field.setPlaceholderText("Descripción breve de la actividad...")
        self.description_field.setFixedHeight(50)
        self.description_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) 
        
        # Orden ajustado: Job antes de interrupciones
        form_layout.addRow("Fecha:", self.date_field)
        form_layout.addRow("Inicio:", self.start_time_field)
        form_layout.addRow("Fin:", self.end_time_field)
        form_layout.addRow("Job:", self.job_field)
        form_layout.addRow("Interrupciones:", self.interruptions_field)
        form_layout.addRow("Descripción:", self.description_field)

        # Botón principal del formulario
        self.save_button = QPushButton("Guardar actividad")
        self.save_button.setObjectName("primaryButton")
        form_layout.addRow(self.save_button)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # =====================================
        # Sección tabla dentro de un GroupBox
        # =====================================
        table_group = QGroupBox("Actividades registradas")
        table_layout = QVBoxLayout()

        # Botones CRUD arriba de la tabla
        buttons_layout = QHBoxLayout()
        self.edit_button = QPushButton("Editar seleccionada")
        self.delete_button = QPushButton("Eliminar seleccionada")
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addStretch()

        table_layout.addLayout(buttons_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Inicio", "Fin", "Interrupciones", "Job", "Descripción"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setMinimumHeight(250)

        # Placeholder temporal
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem("15/06/2026"))
        self.table.setItem(0, 1, QTableWidgetItem("08:00"))
        self.table.setItem(0, 2, QTableWidgetItem("10:00"))
        self.table.setItem(0, 3, QTableWidgetItem("0"))
        self.table.setItem(0, 4, QTableWidgetItem("Login"))
        self.table.setItem(0, 5, QTableWidgetItem("Implementación inicial"))

        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)

        main_layout.addWidget(table_group)

        self.setLayout(main_layout)
