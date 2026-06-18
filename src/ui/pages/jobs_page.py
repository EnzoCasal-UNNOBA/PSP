from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


class JobsPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # --- Formulario arriba ---
        form_layout = QFormLayout()

        self.name_field = QLineEdit()
        self.type_field = QLineEdit()
        self.estimated_time_field = QSpinBox()
        self.estimated_time_field.setRange(1, 1000)
        self.units_field = QSpinBox()
        self.units_field.setRange(1, 1000)

        form_layout.addRow("Nombre:", self.name_field)
        form_layout.addRow("Tipo de tarea:", self.type_field)
        form_layout.addRow("Tiempo estimado:", self.estimated_time_field)
        form_layout.addRow("Unidades estimadas:", self.units_field)

        self.save_button = QPushButton("Guardar Job")

        form_container = QVBoxLayout()
        form_container.addLayout(form_layout)
        form_container.addWidget(self.save_button)

        main_layout.addLayout(form_container)

        # --- Tabla abajo ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Nombre", "Tipo de tarea", "Tiempo estimado", "Unidades"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ejemplo de fila placeholder
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem("Login"))
        self.table.setItem(0, 1, QTableWidgetItem("Implementación"))
        self.table.setItem(0, 2, QTableWidgetItem("4"))
        self.table.setItem(0, 3, QTableWidgetItem("10"))

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
