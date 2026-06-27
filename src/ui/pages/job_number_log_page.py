from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
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
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(280)
        self.table.setSortingEnabled(True)

        # Placeholder
        datos = [
            ["1","15/07","Comunicación","120","1","105","1","105","105","1","105","105","105"],
            ["2","15/07","Esp. Req.","400","1","550","1","550","550","1","550","550","550"],
            ["3","18/07","Seguimiento","300","1","175","1","175","175","1","175","175","175"],
            ["4","19/07","Planificación","300","2","565","2","282.5","565","2","282.5","282.5","282.5"],
            ["5","18/07","Comunicación","100","1","195","1","195","300","2","150","195","105"]
        ]

        for fila, valores in enumerate(datos):
            self.table.insertRow(fila)
            for columna, valor in enumerate(valores):
                self.table.setItem(fila, columna, QTableWidgetItem(valor))

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
