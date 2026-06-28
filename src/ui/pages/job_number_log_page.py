from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QGroupBox
)


class JobNumberLogPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # =====================================================
        # Título
        # =====================================================

        title = QLabel("Job Number Log")
        title.setObjectName("pageTitle")

        main_layout.addWidget(title)

        # =====================================================
        # Acciones
        # =====================================================

        action_group = QGroupBox("Reporte")

        action_layout = QHBoxLayout()

        action_layout.addStretch()

        self.export_button = QPushButton("Exportar CSV")
        self.export_button.setObjectName("primaryButton")

        action_layout.addWidget(self.export_button)

        action_group.setLayout(action_layout)

        main_layout.addWidget(action_group)

        # =====================================================
        # Tabla
        # =====================================================

        table_group = QGroupBox("Historial de Jobs")

        table_layout = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(12)

        self.table.setHorizontalHeaderLabels([
            "Job",
            "Fecha",
            "Proceso",
            "Est. Tiempo",
            "Est. Unid.",
            "Real Tiempo",
            "Real Unid.",
            "Velocidad",
            "Acum Tiempo",
            "Acum Unid.",
            "Máx.",
            "Mín."
        ])

        self.table.setAlternatingRowColors(True)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        table_layout.addWidget(self.table)

        table_group.setLayout(table_layout)

        main_layout.addWidget(table_group)

        self.setLayout(main_layout)