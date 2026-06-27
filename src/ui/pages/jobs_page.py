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
    QHeaderView,
    QAbstractItemView,
    QGroupBox
)


class JobsPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # =====================================================
        # Título
        # =====================================================
        title = QLabel("Jobs")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        description = QLabel("Administración de Jobs PSP y sus estimaciones.")
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # =====================================================
        # Formulario
        # =====================================================
        form_group = QGroupBox("Registrar Job")
        form_layout = QFormLayout()

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Ej.: Implementación Login")

        self.category_field = QComboBox()
        self.category_field.addItem("Seleccione una categoría")

        self.estimated_time_field = QSpinBox()
        self.estimated_time_field.setRange(1, 100000)
        self.estimated_time_field.setSuffix(" min")

        self.units_field = QSpinBox()
        self.units_field.setRange(1, 999)

        form_layout.addRow("Nombre:", self.name_field)
        form_layout.addRow("Categoría:", self.category_field)
        form_layout.addRow("Tiempo estimado:", self.estimated_time_field)
        form_layout.addRow("Unidades estimadas:", self.units_field)

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
            "ID", "Nombre", "Categoría", "Tiempo Est.", "Unidades"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(280)
        self.table.setSortingEnabled(True)

        # Distribución porcentual de columnas
        self.porcentajes = {
            0: 0.08,   # ID → 8%
            1: 0.30,   # Nombre → 30%
            2: 0.25,   # Categoría → 25%
            3: 0.22,   # Tiempo Est. → 22%
            4: 0.15    # Unidades → 15%
        }

        # Ajustar columnas dinámicamente al redimensionar
        self.table.resizeEvent = self.resize_columns

        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)

        self.setLayout(main_layout)

    def resize_columns(self, event):
        ancho_total = self.table.viewport().width()
        for col, pct in self.porcentajes.items():
            self.table.setColumnWidth(col, int(ancho_total * pct))
        super().resizeEvent(event)
