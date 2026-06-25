from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QGroupBox
)


class JobsPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # Título
        title = QLabel("Jobs")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # Formulario
        form_group = QGroupBox("Registrar Job")
        form_layout = QFormLayout()

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Nombre del Job...")

        self.category_field = QComboBox()
        self.category_field.addItem("Seleccionar categoría...")

        self.estimated_time_field = QSpinBox()
        self.estimated_time_field.setRange(1, 1000)

        self.units_field = QSpinBox()
        self.units_field.setRange(1, 1000)

        form_layout.addRow("Nombre:", self.name_field)
        form_layout.addRow("Categoría:", self.category_field)
        form_layout.addRow("Tiempo estimado:", self.estimated_time_field)
        form_layout.addRow("Unidades estimadas:", self.units_field)

        # Botón principal
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.new_button = QPushButton("Nuevo Job")
        self.new_button.setObjectName("primaryButton")
        button_layout.addWidget(self.new_button)

        form_container = QVBoxLayout()
        form_container.addLayout(form_layout)
        form_container.addLayout(button_layout)
        form_group.setLayout(form_container)

        main_layout.addWidget(form_group)

        # Tabla
        table_group = QGroupBox("Jobs registrados")
        table_layout = QVBoxLayout()

        crud_layout = QHBoxLayout()
        self.edit_button = QPushButton("Editar seleccionado")
        self.delete_button = QPushButton("Eliminar seleccionado")
        crud_layout.addWidget(self.edit_button)
        crud_layout.addWidget(self.delete_button)
        crud_layout.addStretch()
        table_layout.addLayout(crud_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Categoría", "Tiempo Est.", "Unidades"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Placeholder
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem("1"))
        self.table.setItem(0, 1, QTableWidgetItem("Login sistema óptica"))
        self.table.setItem(0, 2, QTableWidgetItem("Programación"))
        self.table.setItem(0, 3, QTableWidgetItem("10"))
        self.table.setItem(0, 4, QTableWidgetItem("5"))

        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)

        main_layout.addWidget(table_group)

        self.setLayout(main_layout)
