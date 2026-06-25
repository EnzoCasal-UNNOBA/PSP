from PySide6.QtCore import QDate

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
    QSpinBox,
    QAbstractItemView
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
        # Formulario
        # =====================================

        form_layout = QFormLayout()

        self.date_field = QDateEdit()
        self.date_field.setCalendarPopup(True)
        self.date_field.setDisplayFormat("dd/MM/yyyy")
        self.date_field.setDate(QDate.currentDate())

        self.start_time_field = QTimeEdit()
        self.start_time_field.setDisplayFormat("HH:mm")

        self.end_time_field = QTimeEdit()
        self.end_time_field.setDisplayFormat("HH:mm")

        self.interruptions_field = QSpinBox()
        self.interruptions_field.setRange(0, 999)

        self.job_field = QComboBox()
        self.job_field.addItem("Seleccionar Job...")
        self.job_field.setCurrentIndex(0)

        self.description_field = QTextEdit()
        self.description_field.setFixedHeight(70)
        self.description_field.setPlaceholderText(
            "Descripción breve de la actividad..."
        )

        form_layout.addRow("Fecha:", self.date_field)
        form_layout.addRow("Inicio:", self.start_time_field)
        form_layout.addRow("Fin:", self.end_time_field)
        form_layout.addRow("Interrupciones:", self.interruptions_field)
        form_layout.addRow("Job:", self.job_field)
        form_layout.addRow("Descripción:", self.description_field)

        # =====================================
        # Botones
        # =====================================

        self.save_button = QPushButton("Nueva actividad")
        self.save_button.setObjectName("primaryButton")

        self.edit_button = QPushButton("Editar seleccionada")
        self.delete_button = QPushButton("Eliminar seleccionada")

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)

        form_container = QVBoxLayout()
        form_container.addLayout(form_layout)
        form_container.addLayout(buttons_layout)

        main_layout.addLayout(form_container)

        # =====================================
        # Sección tabla
        # =====================================

        activities_label = QLabel("Actividades registradas")
        activities_label.setObjectName("sectionTitle")

        main_layout.addWidget(activities_label)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Fecha",
            "Inicio",
            "Fin",
            "Interrupciones",
            "Job",
            "Descripción"
        ])

        self.table.setAlternatingRowColors(True)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setMinimumHeight(250)

        # Placeholder temporal de desarrollo

        self.table.insertRow(0)

        self.table.setItem(
            0, 0,
            QTableWidgetItem("15/06/2026")
        )

        self.table.setItem(
            0, 1,
            QTableWidgetItem("08:00")
        )

        self.table.setItem(
            0, 2,
            QTableWidgetItem("10:00")
        )

        self.table.setItem(
            0, 3,
            QTableWidgetItem("0")
        )

        self.table.setItem(
            0, 4,
            QTableWidgetItem("Login")
        )

        self.table.setItem(
            0, 5,
            QTableWidgetItem("Implementación inicial")
        )

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)