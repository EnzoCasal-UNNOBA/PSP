from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy
)


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # ======================================================
        # Título
        # ======================================================

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        main_layout.addWidget(title)

        description = QLabel(
            "Resumen general del proyecto PSP. "
            "Las métricas se actualizarán automáticamente a medida que se registren actividades."
        )
        description.setWordWrap(True)

        main_layout.addWidget(description)

        # ======================================================
        # Tarjetas
        # ======================================================

        cards_layout = QHBoxLayout()

        cards_layout.addWidget(
            self.create_card(
                "Jobs",
                "12"
            )
        )

        cards_layout.addWidget(
            self.create_card(
                "Actividades",
                "58"
            )
        )

        cards_layout.addWidget(
            self.create_card(
                "Horas registradas",
                "84 h"
            )
        )

        cards_layout.addWidget(
            self.create_card(
                "Semana actual",
                "3"
            )
        )

        main_layout.addLayout(cards_layout)

        # ======================================================
        # Panel inferior
        # ======================================================

        panel = QFrame()
        panel.setObjectName("dashboardPanel")

        panel_layout = QVBoxLayout(panel)

        subtitle = QLabel("Información")
        subtitle.setStyleSheet("font-size:16px;font-weight:bold;")

        panel_layout.addWidget(subtitle)

        info = QLabel(
            "• Total de actividades registradas.\n\n"
            "• Tiempo invertido por tipo de tarea.\n\n"
            "• Promedio de velocidad por Job.\n\n"
            "• Próximamente podrán visualizarse gráficos de tendencia."
        )

        info.setWordWrap(True)

        panel_layout.addWidget(info)

        panel_layout.addStretch()

        main_layout.addWidget(panel)

        self.setLayout(main_layout)

    # ==========================================================
    # Tarjeta reutilizable
    # ==========================================================

    def create_card(self, title, value):

        card = QFrame()
        card.setObjectName("dashboardCard")
        card.setFrameShape(QFrame.StyledPanel)

        card.setMinimumHeight(120)
        card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            "font-size:14px;"
            "color:gray;"
        )

        value_label = QLabel(value)
        value_label.setStyleSheet(
            "font-size:28px;"
            "font-weight:bold;"
        )

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)

        return card