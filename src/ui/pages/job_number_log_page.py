from PySide6.QtWidgets import (
    QComboBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QGroupBox,
)
from PySide6.QtCore import Qt
from services.job_number_log_service import (
    get_job_number_log,
)
from services.weekly_summary_service import get_available_weeks

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
        # Filtros
        # =====================================================

        filter_group = QGroupBox("Reporte")

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

        # =====================================================
        # Tabla
        # =====================================================

        table_group = QGroupBox("Historial de Jobs")

        table_layout = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(11)

        self.table.setHorizontalHeaderLabels([
            "Job ID",
            "Fecha",
            "Categoría",
            "T. Est.",
            "Unidades",
            "T. Real",
            "Velocidad",
            "Acum. Tiempo",
            "Promedio",
            "Máx.",
            "Mín."
        ])

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        table_layout.addWidget(self.table)

        table_group.setLayout(table_layout)

        main_layout.addWidget(table_group)

        self.setLayout(main_layout)

        # =====================================================
        # Inicialización
        # =====================================================

        self.load_weeks()

        self.week_selector.currentIndexChanged.connect(
            self.load_table
        )

        self.load_table()

    def load_weeks(self):

        self.week_selector.clear()

        semanas = get_available_weeks()

        for numero, fecha in semanas:

            self.week_selector.addItem(
                f"Semana {numero}",
                fecha
            )
    def load_table(self):

        registros = get_job_number_log()

        self.table.setRowCount(0)

        fila = 0

        for job in registros:

            # ============================
            # Primera fila (datos)
            # ============================

            self.table.insertRow(fila)
            self.table.insertRow(fila + 1)

            self.table.setItem(
                fila,
                0,
                QTableWidgetItem(str(job["job_id"]))
            )

            self.table.setItem(
                fila,
                1,
                QTableWidgetItem(job["fecha"])
            )

            self.table.setItem(
                fila,
                2,
                QTableWidgetItem(job["categoria"])
            )

            self.table.setItem(
                fila,
                3,
                QTableWidgetItem(
                    "" if job["estimado_tiempo"] is None
                    else str(job["estimado_tiempo"])
                )
            )

            self.table.setItem(
                fila,
                4,
                QTableWidgetItem(
                    "" if job["estimado_unidades"] is None
                    else str(job["estimado_unidades"])
                )
            )

            self.table.setItem(
                fila,
                5,
                QTableWidgetItem(str(job["tiempo_real"]))
            )

            self.table.setItem(
                fila,
                6,
                QTableWidgetItem(f"{job['velocidad']:.2f}")
            )

            self.table.setItem(
                fila,
                7,
                QTableWidgetItem(str(job["acumulado"]))
            )

            self.table.setItem(
                fila,
                8,
                QTableWidgetItem(f"{job['velocidad']:.2f}")
            )

            self.table.setItem(
                fila,
                9,
                QTableWidgetItem(str(job["maximo"]))
            )

            self.table.setItem(
                fila,
                10,
                QTableWidgetItem(str(job["minimo"]))
            )

            # =====================================
            # Segunda fila (Nombre del Job)
            # =====================================

            self.table.setSpan(
                fila + 1,
                0,
                1,
                11
            )

            item = QTableWidgetItem(job["job_nombre"])

            item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(
                fila + 1,
                0,
                item
            )

            fila += 2

        self.table.resizeRowsToContents()