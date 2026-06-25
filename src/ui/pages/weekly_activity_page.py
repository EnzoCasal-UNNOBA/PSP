from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton
)


class WeeklyActivityPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # Encabezado
        main_layout.addWidget(QLabel("Weekly Activity"))

        # Selector de semana
        self.week_selector = QComboBox()
        self.week_selector.addItem("Semana 1")  # placeholder
        self.week_selector.addItem("Semana 2")
        main_layout.addWidget(self.week_selector)

        # Tabla de actividades
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Tipo", "Tiempo", "Interrupciones", "Descripción"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ejemplo de fila placeholder
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem("15/06/2026"))
        self.table.setItem(0, 1, QTableWidgetItem("Implementación"))
        self.table.setItem(0, 2, QTableWidgetItem("2h"))
        self.table.setItem(0, 3, QTableWidgetItem("0"))
        self.table.setItem(0, 4, QTableWidgetItem("Login inicial"))

        main_layout.addWidget(self.table)

        # Botón exportar
        self.export_button = QPushButton("Exportar CSV")
        main_layout.addWidget(self.export_button)

        self.setLayout(main_layout)
        
        