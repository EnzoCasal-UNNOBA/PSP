from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QHBoxLayout
)


class CategoriesPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # --- Botones CRUD arriba ---
        buttons_layout = QHBoxLayout()

        self.new_button = QPushButton("Nueva")
        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Eliminar")

        buttons_layout.addWidget(self.new_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        # --- Tabla de categorías ---
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ejemplo de fila placeholder
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem("1"))
        self.table.setItem(0, 1, QTableWidgetItem("Backend"))

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
