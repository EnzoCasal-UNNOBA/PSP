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
    get_week_categories,
    get_weekly_statistics
)

from database.database import get_connection


class WeeklyActivityPage(QWidget):

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
        # Tabla principal (sin columnas fijas)
        # =====================================================
        table_group = QGroupBox("Resumen semanal")
        table_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
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
        # Estadísticas (sin columnas fijas)
        # =====================================================
        stats_group = QGroupBox("Estadísticas")
        stats_layout = QVBoxLayout()

        self.stats_table = QTableWidget()
        self.stats_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.stats_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.stats_table.verticalHeader().setVisible(False)
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        stats_layout.addWidget(self.stats_table)
        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)

        # ==========================================
        # Conexiones
        # ==========================================
        self.week_selector.currentIndexChanged.connect(self.load_selected_week)

        # ==========================================
        # Carga inicial
        # ==========================================
        self.load_weeks()
        self.columnas = {}
        self.setLayout(main_layout)


    def load_weeks(self):
        self.week_selector.clear()
        semanas = get_available_weeks()

        for numero, fecha in semanas:
            self.week_selector.addItem(f"Semana {numero}", fecha)

        if self.week_selector.count() > 0:
            self.week_selector.setCurrentIndex(self.week_selector.count() - 1)

    def load_selected_week(self):
        fecha_inicio = self.week_selector.currentData()
        if not fecha_inicio:
            return

        numero = self.week_selector.currentIndex() + 1
        self.week_number_label.setText(f"Número de semana: {numero}")

        # Definir columnas dinámicas
        categorias = get_week_categories(fecha_inicio)
        self.table.setColumnCount(len(categorias) + 2)  # Fecha + categorías + Totales
        headers = ["Fecha"] + categorias + ["Totales"]
        self.table.setHorizontalHeaderLabels(headers)

        # Guardar mapeo dinámico
        self.columnas = {categoria: i+1 for i, categoria in enumerate(categorias)}

        self.fill_week_table(fecha_inicio)
        self.fill_statistics(fecha_inicio, categorias)

    def fill_week_table(self, fecha_inicio):
        resumen = get_per_day_summary(fecha_inicio)
        daily_totals = get_daily_totals(fecha_inicio)
        weekly_totals = get_weekly_totals(fecha_inicio)

        self.table.setRowCount(8)  # 7 días + Totales
        dias = list(resumen.keys())

        for fila, fecha in enumerate(dias):
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
            self.table.setItem(fila, 0, QTableWidgetItem(fecha_dt.strftime("%d/%m")))

            for categoria, minutos in resumen[fecha].items():
                columna = self.columnas[categoria]
                self.table.setItem(fila, columna, QTableWidgetItem(str(minutos)))

            # Totales por día
            self.table.setItem(fila, len(self.columnas) + 1, QTableWidgetItem(str(daily_totals.get(fecha, 0))))

        # Totales de la semana
        fila_totales = 7
        self.table.setItem(fila_totales, 0, QTableWidgetItem("TOTAL"))

        total_general = 0
        for categoria, columna in self.columnas.items():
            valor = weekly_totals.get(categoria, 0)
            total_general += valor
            self.table.setItem(fila_totales, columna, QTableWidgetItem(str(valor)))

        self.table.setItem(fila_totales, len(self.columnas) + 1, QTableWidgetItem(str(total_general)))
    def fill_statistics(self, fecha_inicio, categorias):
        estadisticas = get_weekly_statistics(fecha_inicio)

        self.stats_table.setColumnCount(len(categorias) + 2)
        self.stats_table.setHorizontalHeaderLabels([""] + categorias + ["Total"])
        self.stats_table.setRowCount(4)

        etiquetas = ["Total", "Promedio", "Máximo", "Mínimo"]
        for fila, texto in enumerate(etiquetas):
            self.stats_table.setItem(fila, 0, QTableWidgetItem(texto))

        total_general = promedio_general = maximo_general = minimo_general = 0

        for categoria in categorias:
            columna = self.columnas[categoria]
            datos = estadisticas.get(categoria)
            if not datos:
                continue

            self.stats_table.setItem(0, columna, QTableWidgetItem(str(datos["total"])))
            self.stats_table.setItem(1, columna, QTableWidgetItem(str(datos["promedio"])))
            self.stats_table.setItem(2, columna, QTableWidgetItem(str(datos["maximo"])))
            self.stats_table.setItem(3, columna, QTableWidgetItem(str(datos["minimo"])))

            total_general += datos["total"]
            promedio_general += datos["promedio"]
            maximo_general = max(maximo_general, datos["maximo"])
            minimo_general = min(minimo_general, datos["minimo"]) if minimo_general else datos["minimo"]

        # Totales generales
        self.stats_table.setItem(0, len(categorias) + 1, QTableWidgetItem(str(total_general)))
        self.stats_table.setItem(1, len(categorias) + 1, QTableWidgetItem(str(round(promedio_general / len(categorias), 2))))
        self.stats_table.setItem(2, len(categorias) + 1, QTableWidgetItem(str(maximo_general)))
        self.stats_table.setItem(3, len(categorias) + 1, QTableWidgetItem(str(minimo_general)))
