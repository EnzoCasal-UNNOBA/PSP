from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QGroupBox,
    QMessageBox
)

from services.task_type_service import (
    create_task_type,
    get_active_task_types,
    update_task_type,
    delete_task_type
)


class CategoriesPage(QWidget):

    def __init__(self):
        super().__init__()

        self.selected_id = None

        # =====================================================
        # Layout principal
        # =====================================================

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # =====================================================
        # Título
        # =====================================================

        title = QLabel("Tipos de tarea")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        description = QLabel(
            "Administración de los tipos de tarea utilizados por los Jobs."
        )
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # =====================================================
        # Formulario
        # =====================================================

        form_group = QGroupBox("Registrar tipo de tarea")
        form_layout = QFormLayout()

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText(
            "Ej.: Diseño, Codificación, Revisión..."
        )

        form_layout.addRow("Nombre:", self.name_field)

        self.new_button = QPushButton("Guardar tipo")
        self.new_button.setObjectName("primaryButton")

        form_layout.addRow(self.new_button)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # =====================================================
        # Tabla
        # =====================================================

        table_group = QGroupBox("Tipos registrados")
        table_layout = QVBoxLayout()

        crud_layout = QHBoxLayout()

        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Eliminar")

        crud_layout.addWidget(self.edit_button)
        crud_layout.addWidget(self.delete_button)
        crud_layout.addStretch()

        table_layout.addLayout(crud_layout)

        self.table = QTableWidget()

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Nombre"
        ])

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )
        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(280)

        self.porcentajes = {
            0: 0.15,
            1: 0.85
        }

        table_layout.addWidget(self.table)

        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)

        self.setLayout(main_layout)

        # =====================================================
        # Conexiones
        # =====================================================

        self.new_button.clicked.connect(self.save_category)
        self.edit_button.clicked.connect(self.load_selected_category)
        self.delete_button.clicked.connect(self.delete_selected_category)

        self.table.itemDoubleClicked.connect(
            self.load_selected_category
        )

        # =====================================================
        # Carga inicial
        # =====================================================

        self.load_categories()

    # =====================================================
    # CRUD
    # =====================================================

    def load_categories(self):

        self.table.setRowCount(0)

        categorias = get_active_task_types()

        for fila, categoria in enumerate(categorias):

            self.table.insertRow(fila)

            self.table.setItem(
                fila,
                0,
                QTableWidgetItem(str(categoria[0]))
            )

            self.table.setItem(
                fila,
                1,
                QTableWidgetItem(categoria[1])
            )

        self.resize_columns()

    def save_category(self):

        nombre = self.name_field.text()

        try:

            if self.selected_id is None:

                create_task_type(nombre)

                QMessageBox.information(
                    self,
                    "Éxito",
                    "Tipo de tarea creado correctamente."
                )

            else:

                update_task_type(
                    self.selected_id,
                    nombre
                )

                QMessageBox.information(
                    self,
                    "Éxito",
                    "Tipo de tarea actualizado correctamente."
                )

            self.clear_form()
            self.load_categories()

        except ValueError as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def load_selected_category(self):

        fila = self.table.currentRow()

        if fila < 0:

            QMessageBox.warning(
                self,
                "Atención",
                "Seleccione un tipo de tarea."
            )
            return

        self.selected_id = int(
            self.table.item(fila, 0).text()
        )

        self.name_field.setText(
            self.table.item(fila, 1).text()
        )

        self.new_button.setText("Actualizar tipo")

    def delete_selected_category(self):

        fila = self.table.currentRow()

        if fila < 0:

            QMessageBox.warning(
                self,
                "Atención",
                "Seleccione un tipo de tarea."
            )
            return

        categoria_id = int(
            self.table.item(fila, 0).text()
        )

        respuesta = QMessageBox.question(
            self,
            "Eliminar",
            "¿Desea eliminar este tipo de tarea?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return

        try:

            delete_task_type(categoria_id)

            QMessageBox.information(
                self,
                "Éxito",
                "Tipo de tarea eliminado correctamente."
            )

            self.clear_form()
            self.load_categories()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    # =====================================================
    # Helpers
    # =====================================================

    def clear_form(self):

        self.selected_id = None

        self.name_field.clear()

        self.new_button.setText("Guardar tipo")

        self.table.clearSelection()

    def resize_columns(self):

        ancho = self.table.viewport().width()

        self.table.setColumnWidth(
            0,
            int(ancho * 0.15)
        )

        self.table.setColumnWidth(
            1,
            int(ancho * 0.85)
        )

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self.resize_columns()