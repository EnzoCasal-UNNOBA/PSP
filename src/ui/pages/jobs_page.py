from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QGroupBox,
    QMessageBox
)

from services.job_service import (
    get_all_active_jobs,
    get_job_by_id,
    create_job,
    update_job,
    delete_job
)

from services.task_type_service import (
    get_active_task_types
)


class JobsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.selected_id = None

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # =====================================================
        # Título
        # =====================================================

        title = QLabel("Jobs")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        description = QLabel(
            "Administración de los trabajos utilizados por el Daily Log."
        )
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # =====================================================
        # Formulario
        # =====================================================

        form_group = QGroupBox("Registrar Job")

        form_layout = QFormLayout()

        # Nombre

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Nombre del Job")

        form_layout.addRow(
            "Nombre:",
            self.name_field
        )

        # Tipo de tarea

        self.task_type_field = QComboBox()

        form_layout.addRow(
            "Tipo:",
            self.task_type_field
        )

        # Tiempo estimado

        self.time_field = QSpinBox()
        self.time_field.setRange(0, 999999)
        self.time_field.setSpecialValueText("")

        form_layout.addRow(
            "Tiempo estimado:",
            self.time_field
        )

        # Unidades estimadas

        self.units_field = QDoubleSpinBox()
        self.units_field.setRange(0, 999999)
        self.units_field.setDecimals(2)
        self.units_field.setSpecialValueText("")

        form_layout.addRow(
            "Unidades estimadas:",
            self.units_field
        )

        # Botón guardar

        self.new_button = QPushButton("Guardar Job")
        self.new_button.setObjectName("primaryButton")

        form_layout.addRow(self.new_button)

        form_group.setLayout(form_layout)

        main_layout.addWidget(form_group)

        # =====================================================
        # Tabla
        # =====================================================

        table_group = QGroupBox("Jobs registrados")

        table_layout = QVBoxLayout()

        crud_layout = QHBoxLayout()

        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Eliminar")

        crud_layout.addWidget(self.edit_button)
        crud_layout.addWidget(self.delete_button)
        crud_layout.addStretch()

        table_layout.addLayout(crud_layout)

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Nombre",
            "Tipo",
            "Tiempo Est.",
            "Unidades Est."
        ])

        self.table.setAlternatingRowColors(True)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setMinimumHeight(300)

        self.table.setSortingEnabled(True)

        self.porcentajes = {
            0: 0.08,
            1: 0.34,
            2: 0.26,
            3: 0.16,
            4: 0.16
        }

        self.table.resizeEvent = self.resize_columns

        table_layout.addWidget(self.table)

        table_group.setLayout(table_layout)

        main_layout.addWidget(table_group)

        self.setLayout(main_layout)

        # =====================================================
        # Conexiones
        # =====================================================

        self.new_button.clicked.connect(self.save_job)

        self.edit_button.clicked.connect(
            self.load_selected_job
        )

        self.delete_button.clicked.connect(
            self.delete_selected_job
        )

        self.table.itemDoubleClicked.connect(
            self.load_selected_job
        )

        # =====================================================
        # Carga inicial
        # =====================================================

        self.load_task_types()

        self.load_jobs()


    # =====================================================
    # Carga de datos
    # =====================================================

    def load_task_types(self):
        """Carga los tipos de tarea activos en el ComboBox."""

        self.task_type_field.clear()

        task_types = get_active_task_types()

        for task_type in task_types:
            self.task_type_field.addItem(
                task_type[1],      # Nombre visible
                task_type[0]       # ID oculto
            )


    def load_jobs(self):
        """Carga todos los Jobs activos."""

        jobs = get_all_active_jobs()

        self.table.setRowCount(len(jobs))

        for fila, job in enumerate(jobs):

            self.table.setItem(
                fila,
                0,
                QTableWidgetItem(str(job[0]))
            )

            self.table.setItem(
                fila,
                1,
                QTableWidgetItem(job[1])
            )

            self.table.setItem(
                fila,
                2,
                QTableWidgetItem(job[2])
            )

            tiempo = "" if job[3] is None else str(job[3])

            unidades = "" if job[4] is None else str(job[4])

            self.table.setItem(
                fila,
                3,
                QTableWidgetItem(tiempo)
            )

            self.table.setItem(
                fila,
                4,
                QTableWidgetItem(unidades)
            )

        self.resize_columns()


    # =====================================================
    # Helpers
    # =====================================================

    def clear_form(self):
        """Limpia el formulario."""

        self.selected_id = None

        self.name_field.clear()

        self.task_type_field.setCurrentIndex(0)

        self.time_field.setValue(0)

        self.units_field.setValue(0)

        self.new_button.setText("Guardar Job")

        self.table.clearSelection()
    
    # =====================================================
    # CRUD
    # =====================================================

    def load_selected_job(self):

        fila = self.table.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Atención",
                "Seleccione un Job."
            )
            return

        self.selected_id = int(
            self.table.item(fila, 0).text()
        )

        job = get_job_by_id(self.selected_id)

        if job is None:
            return

        self.name_field.setText(job[1])

        index = self.task_type_field.findData(job[2])

        if index >= 0:
            self.task_type_field.setCurrentIndex(index)

        self.time_field.setValue(job[4] or 0)

        self.units_field.setValue(job[5] or 0)

        self.new_button.setText("Actualizar Job")

    def save_job(self):

        nombre = self.name_field.text()

        tipo_tarea_id = self.task_type_field.currentData()

        tiempo = self.time_field.value()
        unidades = self.units_field.value()

        # Si quedaron en 0 se envían como NULL
        if tiempo == 0:
            tiempo = None

        if unidades == 0:
            unidades = None

        try:

            if self.selected_id is None:

                create_job(
                    nombre,
                    tipo_tarea_id,
                    tiempo,
                    unidades
                )

                QMessageBox.information(
                    self,
                    "Éxito",
                    "Job creado correctamente."
                )

            else:

                update_job(
                    self.selected_id,
                    nombre,
                    tipo_tarea_id,
                    tiempo,
                    unidades
                )

                QMessageBox.information(
                    self,
                    "Éxito",
                    "Job actualizado correctamente."
                )

            self.clear_form()
            self.load_jobs()

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error)
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )


    def delete_selected_job(self):

        fila = self.table.currentRow()

        if fila < 0:

            QMessageBox.warning(
                self,
                "Atención",
                "Seleccione un Job."
            )

            return

        job_id = int(
            self.table.item(fila, 0).text()
        )

        respuesta = QMessageBox.question(
            self,
            "Eliminar",
            "¿Desea eliminar este Job?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return

        try:

            delete_job(job_id)

            QMessageBox.information(
                self,
                "Éxito",
                "Job eliminado correctamente."
            )

            self.clear_form()

            self.load_jobs()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )


    def resize_columns(self, event=None):

        ancho = self.table.viewport().width()

        for columna, porcentaje in self.porcentajes.items():

            self.table.setColumnWidth(
                columna,
                int(ancho * porcentaje)
            )

        if event:
            super().resizeEvent(event)