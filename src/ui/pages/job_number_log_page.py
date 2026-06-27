from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QAbstractItemView,
    QGroupBox
)


class JobNumberLogPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # ======================================================
        # Título
        # ======================================================
        title = QLabel("Job Number Log")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # ======================================================
        # Tabla
        # ======================================================
        table_group = QGroupBox("Registro histórico")
        table_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels([
            "# Job",
            "Fecha",
            "Proceso",
            "Tiempo Est.",
            "Unid. Est.",
            "Tiempo Real",
            "Unid. Reales",
            "Velocidad",
            "Tiempo Acum.",
            "Unid. Acum.",
            "Vel. Prom.",
            "Máx.",
            "Mín."
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(280)
        self.table.setSortingEnabled(True)

        # Distribución porcentual de columnas
        self.porcentajes = {
            0: 0.05,   # # Job → 5%
            1: 0.08,   # Fecha → 8%
            2: 0.20,   # Proceso → 20%
            3: 0.08,   # Tiempo Est.
            4: 0.05,   # Unid. Est.
            5: 0.08,   # Tiempo Real
            6: 0.05,   # Unid. Reales
            7: 0.08,   # Velocidad
            8: 0.08,   # Tiempo Acum.
            9: 0.05,   # Unid. Acum.
            10: 0.08,  # Vel. Prom.
            11: 0.06,  # Máx.
            12: 0.06   # Mín.
        }

        # Ajustar anchos después de mostrar la tabla
        self.table.resizeEvent = self.resize_columns

        table_layout.addWidget(self.table)

        # Botón exportar al fondo
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.export_button = QPushButton("Exportar CSV")
        self.export_button.setObjectName("primaryButton")
        bottom_layout.addWidget(self.export_button)

        table_layout.addLayout(bottom_layout)
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)

        self.setLayout(main_layout)

    def resize_columns(self, event):
        ancho_total = self.table.viewport().width()
        for col, pct in self.porcentajes.items():
            self.table.setColumnWidth(col, int(ancho_total * pct))
        super().resizeEvent(event)
