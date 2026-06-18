from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QVBoxLayout,
    QPushButton
)


class ReportsPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # --- Tarjeta Weekly Activity ---
        weekly_group = QGroupBox("Weekly Activity")
        weekly_layout = QVBoxLayout()
        self.btn_weekly_view = QPushButton("Ver reporte")
        self.btn_weekly_generate = QPushButton("Generar reporte")
        weekly_layout.addWidget(self.btn_weekly_view)
        weekly_layout.addWidget(self.btn_weekly_generate)
        weekly_group.setLayout(weekly_layout)

        # --- Tarjeta Job Number Log ---
        joblog_group = QGroupBox("Job Number Log")
        joblog_layout = QVBoxLayout()
        self.btn_joblog_view = QPushButton("Ver reporte")
        self.btn_joblog_generate = QPushButton("Generar reporte")
        joblog_layout.addWidget(self.btn_joblog_view)
        joblog_layout.addWidget(self.btn_joblog_generate)
        joblog_group.setLayout(joblog_layout)

        # --- Tarjeta Exportar ---
        export_group = QGroupBox("Exportar")
        export_layout = QVBoxLayout()
        self.btn_export_csv = QPushButton("Exportar CSV")
        export_layout.addWidget(self.btn_export_csv)
        export_group.setLayout(export_layout)

        # Añadir las tarjetas al layout principal
        main_layout.addWidget(weekly_group)
        main_layout.addWidget(joblog_group)
        main_layout.addWidget(export_group)

        self.setLayout(main_layout)
