from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton
)


class JobNumberLogPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # Encabezado
        main_layout.addWidget(QLabel("Job Number Log"))

        # Tabla de Jobs
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Job #", "Nombre", "Tipo", "Estimado", "Real", "Mínimo", "Máximo"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ejemplo de fila placeholder
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem("1"))
        self.table.setItem(0, 1, QTableWidgetItem("Login"))
        self.table.setItem(0, 2, QTableWidgetItem("Implementación"))
        self.table.setItem(0, 3, QTableWidgetItem("4h"))
        self.table.setItem(0, 4, QTableWidgetItem("5h"))
        self.table.setItem(0, 5, QTableWidgetItem("3h"))
        self.table.setItem(0, 6, QTableWidgetItem("6h"))

        main_layout.addWidget(self.table)

        # Botón exportar
        self.export_button = QPushButton("Exportar CSV")
        main_layout.addWidget(self.export_button)

        self.setLayout(main_layout)
