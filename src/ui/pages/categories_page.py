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
    QHeaderView,
    QAbstractItemView,
    QGroupBox
)


class CategoriesPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # Título
        title = QLabel("Categorías")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # Formulario
        form_group = QGroupBox("Registrar categoría")
        form_layout = QFormLayout()

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Nombre de la categoría...")

        form_layout.addRow("Nombre:", self.name_field)

        # Botón principal
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.new_button = QPushButton("Nueva categoría")
        self.new_button.setObjectName("primaryButton")
        button_layout.addWidget(self.new_button)

        form_container = QVBoxLayout()
        form_container.addLayout(form_layout)
        form_container.addLayout(button_layout)
        form_group.setLayout(form_container)

        main_layout.addWidget(form_group)

        # Tabla
        table_group = QGroupBox("Categorías registradas")
        table_layout = QVBoxLayout()

        crud_layout = QHBoxLayout()
        self.edit_button = QPushButton("Editar seleccionada")
        self.delete_button = QPushButton("Eliminar seleccionada")
        crud_layout.addWidget(self.edit_button)
        crud_layout.addWidget(self.delete_button)
        crud_layout.addStretch()
        table_layout.addLayout(crud_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Placeholder
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem("1"))
        self.table.setItem(0, 1, QTableWidgetItem("Programación"))

        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)

        main_layout.addWidget(table_group)

        self.setLayout(main_layout)
