from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QAbstractItemView,
    QGroupBox
)


class WeeklyActivityPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # ======================================================
        # Título
        # ======================================================
        title = QLabel("Weekly Activity")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # ======================================================
        # Filtros
        # ======================================================
        filter_group = QGroupBox("Reporte semanal")
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Semana"))

        self.week_selector = QComboBox()
        filter_layout.addWidget(self.week_selector)

        filter_layout.addStretch()

        self.export_button = QPushButton("Exportar CSV")
        self.export_button.setObjectName("primaryButton")
        filter_layout.addWidget(self.export_button)

        filter_group.setLayout(filter_layout)
        main_layout.addWidget(filter_group)

        # ======================================================
        # Tabla
        # ======================================================
        table_group = QGroupBox("Resumen semanal")
        table_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setRowCount(8)

        self.table.setHorizontalHeaderLabels([
            "Fecha",
            "Comunicación",
            "Esp. Requisitos",
            "Seguimiento",
            "Planificación",
            "Diseño",
            "Totales"
        ])

        self.table.setVerticalHeaderLabels([
            "L",
            "M",
            "M",
            "J",
            "V",
            "S",
            "D",
            "Totales"
        ])

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)

        self.setLayout(main_layout)
