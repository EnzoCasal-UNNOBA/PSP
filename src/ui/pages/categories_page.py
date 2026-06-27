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
        self.name_field.setPlaceholderText("Ej.: Diseño, Codificación, Revisión...")

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
        self.table.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)  # elimina los números fijos de fila
        self.table.setMinimumHeight(280)
        self.table.setSortingEnabled(True)

        # Distribución porcentual de columnas
        self.porcentajes = {
            0: 0.15,  # ID → 15% del ancho
            1: 0.85   # Nombre → 85% del ancho
        }
        self.table.resizeEvent = self.resize_columns

        # Placeholder con IDs autoincrementales reales
        ejemplos = [
            "Comunicación",
            "Esp. Requisitos",
            "Diseño",
            "Seguimiento",
            "Planificación"
        ]
        for fila, nombre in enumerate(ejemplos):
            self.table.insertRow(fila)
            self.table.setItem(fila, 0, QTableWidgetItem(str(fila + 1)))  # ID autoincremental
            self.table.setItem(fila, 1, QTableWidgetItem(nombre))

        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)

        self.setLayout(main_layout)

    def resize_columns(self, event):
        ancho_total = self.table.viewport().width()
        for col, pct in self.porcentajes.items():
            self.table.setColumnWidth(col, int(ancho_total * pct))
        super().resizeEvent(event)
