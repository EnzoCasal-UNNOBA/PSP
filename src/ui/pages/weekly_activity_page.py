from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
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
        self.week_selector.addItem("Semana 1")
        self.week_selector.addItem("Semana 2")
        self.week_selector.addItem("Semana 3")

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

        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels([
            "Fecha",
            "Comunicación",
            "Esp. Requisitos",
            "Seguimiento",
            "Planificación",
            "Diseño",
            "Totales",
            "Semana"
        ])

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Placeholder

        datos = [
            ["15/07","105","210","","","","315","1"],
            ["16/07","","340","","","","340","1"],
            ["17/07","45","320","","","","365","1"],
            ["18/07","150","","55","","","205","1"],
            ["19/07","","","","355","130","485","1"],
            ["TOTAL","300","870","55","355","130","1710",""]
        ]

        for fila, valores in enumerate(datos):

            self.table.insertRow(fila)

            for columna, valor in enumerate(valores):

                self.table.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(valor)
                )

        table_layout.addWidget(self.table)

        table_group.setLayout(table_layout)

        main_layout.addWidget(table_group)

        self.setLayout(main_layout)