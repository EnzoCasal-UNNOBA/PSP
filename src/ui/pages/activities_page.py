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
    QSizePolicy,
    QSpinBox,
    QAbstractItemView,
    QGroupBox,
    QMessageBox
)

from services.activity_service import (
    create_activity,
    get_all_activities,
    get_activity_by_id,
    update_activity,
    delete_activity
)

from services.job_service import (
    get_all_active_jobs
)


class ActivitiesPage(QWidget):

    def __init__(self):
        super().__init__()

        self.selected_id = None

        main_layout = QVBoxLayout()

        # =====================================================
        # Título
        # =====================================================

        title = QLabel("Daily Log")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # =====================================================
        # Formulario
        # =====================================================

        form_group = QGroupBox("Registrar actividad")
        form_layout = QFormLayout()

        self.date_field = QDateEdit()
        self.date_field.setCalendarPopup(True)
        self.date_field.setDisplayFormat("dd/MM/yyyy")
        self.date_field.setDate(QDate.currentDate())

        self.start_time_field = QTimeEdit()
        self.start_time_field.setDisplayFormat("HH:mm")
        self.start_time_field.setTime(QTime.currentTime()
        )

        self.end_time_field = QTimeEdit()
        self.end_time_field.setDisplayFormat("HH:mm")
        self.end_time_field.setTime(
            QTime.currentTime().addSecs(3600)
        )

        self.job_field = QComboBox()

        self.interruptions_field = QSpinBox()
        self.interruptions_field.setRange(0, 999)

        self.description_field = QTextEdit()
        self.description_field.setPlaceholderText(
            "Descripción..."
        )
        self.description_field.setFixedHeight(60)
        self.description_field.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        form_layout.addRow("Fecha:", self.date_field)
        form_layout.addRow("Inicio:", self.start_time_field)
        form_layout.addRow("Fin:", self.end_time_field)
        form_layout.addRow("Job:", self.job_field)
        form_layout.addRow("Interrupciones:", self.interruptions_field)
        form_layout.addRow("Descripción:", self.description_field)

        self.save_button = QPushButton("Guardar actividad")
        self.save_button.setObjectName("primaryButton")

        form_layout.addRow(self.save_button)

        form_group.setLayout(form_layout)

        main_layout.addWidget(form_group)

        # =====================================================
        # Tabla
        # =====================================================

        table_group = QGroupBox("Actividades registradas")

        table_layout = QVBoxLayout()

        crud_layout = QHBoxLayout()

        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Eliminar")

        crud_layout.addWidget(self.edit_button)
        crud_layout.addWidget(self.delete_button)
        crud_layout.addStretch()

        table_layout.addLayout(crud_layout)

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Fecha",
            "Inicio",
            "Fin",
            "Interrupciones",
            "Job",
            "Descripción"
        ])

        self.table.verticalHeader().setVisible(False)

        self.table.setAlternatingRowColors(True)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.setSortingEnabled(True)

        self.table.setMinimumHeight(300)

        self.porcentajes = {
            0: 0.07,
            1: 0.12,
            2: 0.10,
            3: 0.10,
            4: 0.12,
            5: 0.17,
            6: 0.32
        }

        self.table.resizeEvent = self.resize_columns

        table_layout.addWidget(self.table)

        table_group.setLayout(table_layout)

        main_layout.addWidget(table_group)

        self.setLayout(main_layout)

        # =====================================================
        # Conexiones
        # =====================================================

        self.save_button.clicked.connect(
            self.save_activity
        )

        self.edit_button.clicked.connect(
            self.load_selected_activity
        )

        self.delete_button.clicked.connect(
            self.delete_selected_activity
        )

        self.table.itemDoubleClicked.connect(
            self.load_selected_activity
        )

        # =====================================================
        # Carga inicial
        # =====================================================

        self.load_jobs()
        self.load_activities()

    # =====================================================
    # Cargar Jobs
    # =====================================================

    def load_jobs(self):

        self.job_field.clear()

        jobs = get_all_active_jobs()

        for job in jobs:
            self.job_field.addItem(
                job[1],      # nombre
                job[0]       # id
            )

    def load_activities(self):
        
        activities = get_all_activities()
        

        self.table.setRowCount(len(activities))

        for row, activity in enumerate(activities):

            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(activity[0])))

            # Fecha
            self.table.setItem(row, 1, QTableWidgetItem(activity[1]))

            # Inicio
            self.table.setItem(row, 2, QTableWidgetItem(activity[2]))

            # Fin
            self.table.setItem(row, 3, QTableWidgetItem(activity[3]))

            # Interrupciones
            self.table.setItem(row, 4, QTableWidgetItem(str(activity[4])))

            # Job
            self.table.setItem(row, 5, QTableWidgetItem(activity[7]))

            # Descripción
            self.table.setItem(row, 6, QTableWidgetItem(activity[5]))
        
        self.resize_columns()


    def save_activity(self):

        fecha = self.date_field.date().toString("yyyy-MM-dd")

        hora_inicio = self.start_time_field.time().toString("HH:mm")

        hora_fin = self.end_time_field.time().toString("HH:mm")

        interrupciones = self.interruptions_field.value()

        descripcion = self.description_field.toPlainText()

        job_id = self.job_field.currentData()

        try:

            if self.selected_id is None:
                
                create_activity(
                    fecha,
                    hora_inicio,
                    hora_fin,
                    interrupciones,
                    descripcion,
                    job_id
                )

                QMessageBox.information(
                    self,
                    "Éxito",
                    "Actividad registrada correctamente."
                )

            else:

                update_activity(
                    self.selected_id,
                    fecha,
                    hora_inicio,
                    hora_fin,
                    interrupciones,
                    descripcion,
                    job_id
                )

                QMessageBox.information(
                    self,
                    "Éxito",
                    "Actividad actualizada correctamente."
                )

            self.clear_form()

            self.load_activities()

        except Exception as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error)
            )

    def load_selected_activity(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atención", "Seleccione una actividad.")
            return

        activity_id = int(self.table.item(row, 0).text())
        activity = get_activity_by_id(activity_id)

        self.selected_id = activity[0]

        self.date_field.setDate(QDate.fromString(activity[1], "yyyy-MM-dd"))
        self.start_time_field.setTime(QTime.fromString(activity[2], "HH:mm"))
        self.end_time_field.setTime(QTime.fromString(activity[3], "HH:mm"))
        self.interruptions_field.setValue(activity[4])
        self.description_field.setPlainText(activity[5])

        index = self.job_field.findData(activity[6])
        if index >= 0:
            self.job_field.setCurrentIndex(index)

        self.save_button.setText("Actualizar actividad")


    def delete_selected_activity(self):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Atención",
                "Seleccione una actividad."
            )

            return

        activity_id = int(
            self.table.item(row, 0).text()
        )

        respuesta = QMessageBox.question(
            self,
            "Eliminar",
            "¿Desea eliminar esta actividad?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return

        delete_activity(activity_id)

        QMessageBox.information(
            self,
            "Éxito",
            "Actividad eliminada correctamente."
        )

        self.clear_form()

        self.load_activities()
    # =====================================================
    # Limpiar formulario
    # =====================================================

    def clear_form(self):

        self.selected_id = None

        self.date_field.setDate(QDate.currentDate())

        self.start_time_field.setTime(
            QTime.currentTime()
        )

        self.end_time_field.setTime(
            QTime.currentTime().addSecs(3600)
        )

        self.interruptions_field.setValue(0)

        self.description_field.clear()

        self.job_field.setCurrentIndex(0)

        self.save_button.setText(
            "Guardar actividad"
        )

        self.table.clearSelection()

        # =====================================================
    # Helpers
    # =====================================================

    def resize_columns(self, event=None):

        ancho = self.table.viewport().width()

        for columna, porcentaje in self.porcentajes.items():

            self.table.setColumnWidth(
                columna,
                int(ancho * porcentaje)
            )

        if event:
            super().resizeEvent(event)