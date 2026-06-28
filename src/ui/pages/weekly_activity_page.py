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
from datetime import datetime

from services.weekly_summary_service import (
    get_available_weeks,
    get_per_day_summary,
    get_daily_totals,
    get_weekly_totals,
    get_week_total,
    get_weekly_statistics
)

from database.database import get_connection


class WeeklyActivityPage(QWidget):

    COLUMNAS = {
        "Comunicación": 1,
        "Esp. Requisitos": 2,
        "Seguimiento": 3,
        "Planificación": 4,
        "Diseño": 5
    }

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # =====================================================
        # Título
        # =====================================================

        title = QLabel("Weekly Activity")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        # =====================================================
        # Selector de semana
        # =====================================================

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

        # =====================================================
        # Tabla principal
        # =====================================================

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

        # =====================================================
        # Información de semana
        # =====================================================

        self.week_number_label = QLabel("Número de semana: -")
        main_layout.addWidget(self.week_number_label)

        # =====================================================
        # Estadísticas
        # =====================================================

        stats_group = QGroupBox("Estadísticas")

        stats_layout = QVBoxLayout()

        self.stats_table = QTableWidget()

        self.stats_table.setColumnCount(7)
        self.stats_table.setRowCount(4)

        self.stats_table.setHorizontalHeaderLabels([
            "",
            "Comunicación",
            "Esp. Requisitos",
            "Seguimiento",
            "Planificación",
            "Diseño",
            "Total"
        ])

        self.stats_table.verticalHeader().setVisible(False)

        self.stats_table.setItem(0,0,QTableWidgetItem("Total"))
        self.stats_table.setItem(1,0,QTableWidgetItem("Promedio"))
        self.stats_table.setItem(2,0,QTableWidgetItem("Máximo"))
        self.stats_table.setItem(3,0,QTableWidgetItem("Mínimo"))

        self.stats_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.stats_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        stats_layout.addWidget(self.stats_table)

        stats_group.setLayout(stats_layout)

        main_layout.addWidget(stats_group)

        # ==========================================
        # Conexiones
        # ==========================================

        self.week_selector.currentIndexChanged.connect(
            self.load_selected_week
        )

        # ==========================================
        # Carga inicial
        # ==========================================

        self.load_weeks()
        self.setLayout(main_layout)

    def load_weeks(self):

        self.week_selector.clear()

        conn = get_connection()

        weeks = get_available_weeks(conn)

        conn.close()

        for numero, fecha in enumerate(weeks, start=1):

            self.week_selector.addItem(
                f"Semana {numero}",
                fecha
            )

        if self.week_selector.count() > 0:
            self.week_selector.setCurrentIndex(
                self.week_selector.count() - 1
            )

    def load_selected_week(self):

        fecha_inicio = self.week_selector.currentData()

        if not fecha_inicio:
            return

        numero = self.week_selector.currentIndex() + 1

        self.week_number_label.setText(
            f"Número de semana: {numero}"
        )

        self.fill_week_table(fecha_inicio)

        self.fill_statistics(fecha_inicio)

    def fill_week_table(self, fecha_inicio):

        resumen = get_per_day_summary(fecha_inicio)
        daily_totals = get_daily_totals(fecha_inicio)
        weekly_totals = get_weekly_totals(fecha_inicio)

        self.table.clearContents()

        dias = list(resumen.keys())

        for fila, fecha in enumerate(dias):

            fecha_dt = datetime.strptime(
                fecha,
                "%Y-%m-%d"
            )

            self.table.setItem(
                fila,
                0,
                QTableWidgetItem(
                    fecha_dt.strftime("%d/%m")
                )
            )

            for categoria, minutos in resumen[fecha].items():

                columna = self.COLUMNAS.get(categoria)

                if columna is None:
                    continue

                self.table.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(str(minutos))
                )

            self.table.setItem(
                fila,
                6,
                QTableWidgetItem(
                    str(daily_totals.get(fecha, 0))
                )
            )

        # --------------------------
        # Totales (última fila)
        # --------------------------

        fila_totales = 7

        self.table.setItem(
            fila_totales,
            0,
            QTableWidgetItem("TOTAL")
        )

        total_general = 0

        for categoria, columna in self.COLUMNAS.items():

            valor = weekly_totals.get(categoria, 0)

            total_general += valor

            self.table.setItem(
                fila_totales,
                columna,
                QTableWidgetItem(str(valor))
            )

        self.table.setItem(
            fila_totales,
            6,
            QTableWidgetItem(str(total_general))
        )
    def fill_statistics(self, fecha_inicio):

        estadisticas = get_weekly_statistics(fecha_inicio)

        self.stats_table.clearContents()

        etiquetas = [
            "Total",
            "Promedio",
            "Máximo",
            "Mínimo"
        ]

        for fila, texto in enumerate(etiquetas):

            self.stats_table.setItem(
                fila,
                0,
                QTableWidgetItem(texto)
            )

        total_general = 0
        promedio_general = 0
        maximo_general = 0
        minimo_general = 0

        for categoria, columna in self.COLUMNAS.items():

            datos = estadisticas.get(categoria)

            if not datos:
                continue

            self.stats_table.setItem(
                0,
                columna,
                QTableWidgetItem(str(datos["total"]))
            )

            self.stats_table.setItem(
                1,
                columna,
                QTableWidgetItem(str(datos["promedio"]))
            )

            self.stats_table.setItem(
                2,
                columna,
                QTableWidgetItem(str(datos["maximo"]))
            )

            self.stats_table.setItem(
                3,
                columna,
                QTableWidgetItem(str(datos["minimo"]))
            )

            total_general += datos["total"]
            promedio_general += datos["promedio"]
            maximo_general += datos["maximo"]
            minimo_general += datos["minimo"]

        self.stats_table.setItem(
            0,
            6,
            QTableWidgetItem(str(total_general))
        )

        self.stats_table.setItem(
            1,
            6,
            QTableWidgetItem(str(round(promedio_general, 2)))
        )

        self.stats_table.setItem(
            2,
            6,
            QTableWidgetItem(str(maximo_general))
        )

        self.stats_table.setItem(
            3,
            6,
            QTableWidgetItem(str(minimo_general))
        )