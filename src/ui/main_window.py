from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QApplication
)
from PySide6.QtCore import QSize

from ui.pages.dashboard_page import DashboardPage
from ui.pages.activities_page import ActivitiesPage
from ui.pages.jobs_page import JobsPage
from ui.pages.categories_page import CategoriesPage
from ui.pages.weekly_activity_page import WeeklyActivityPage
from ui.pages.job_number_log_page import JobNumberLogPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PSP Manager")
        self.resize(1200, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # ---------------------------
        # Sidebar
        # ---------------------------
        sidebar = QVBoxLayout()

        # Botón circular para alternar tema
        self.btn_theme = QPushButton("🌙")
        self.btn_theme.setFixedSize(QSize(40, 40))
        self.btn_theme.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: #FFFFFF;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #E0F0FF;
            }
            QPushButton:pressed {
                background-color: #CCE4FF;
            }
        """)
        sidebar.addWidget(self.btn_theme)

        # Botones de navegación
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_activities = QPushButton("Daily Log")
        self.btn_weekly = QPushButton("Weekly Activity")
        self.btn_joblog = QPushButton("Job Number Log")
        self.btn_jobs = QPushButton("Jobs")
        self.btn_categories = QPushButton("Categorías")

        sidebar.addWidget(self.btn_dashboard)
        sidebar.addWidget(self.btn_activities)
        sidebar.addWidget(self.btn_weekly)
        sidebar.addWidget(self.btn_joblog)
        sidebar.addWidget(self.btn_jobs)
        sidebar.addWidget(self.btn_categories)

        sidebar.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setMinimumWidth(220)
        sidebar_widget.setMaximumWidth(220)

        # ---------------------------
        # Páginas
        # ---------------------------
        self.stack = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.activities_page = ActivitiesPage()
        self.weekly_page = WeeklyActivityPage()
        self.joblog_page = JobNumberLogPage()
        self.jobs_page = JobsPage()
        self.categories_page = CategoriesPage()

        self.stack.addWidget(self.dashboard_page)      # 0
        self.stack.addWidget(self.activities_page)     # 1
        self.stack.addWidget(self.weekly_page)         # 2
        self.stack.addWidget(self.joblog_page)         # 3
        self.stack.addWidget(self.jobs_page)           # 4
        self.stack.addWidget(self.categories_page)     # 5

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.stack)

        self.connect_signals()

        # Abrir directamente en Daily Log
        self.stack.setCurrentIndex(1)

        # Estado del tema
        self.dark_mode = False

    def connect_signals(self):
        self.btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_activities.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_weekly.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_joblog.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.btn_jobs.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        self.btn_categories.clicked.connect(lambda: self.stack.setCurrentIndex(5))

        # Botón de tema oscuro
        self.btn_theme.clicked.connect(self.toggle_theme)

    def toggle_theme(self):
        """Alterna entre tema claro y oscuro"""
        if self.dark_mode:
            # volver a tema claro
            QApplication.instance().setStyleSheet(
                open("src/ui/styles/light_theme.qss").read()
            )
            self.btn_theme.setText("🌙")
            self.dark_mode = False
        else:
            # aplicar tema oscuro
            QApplication.instance().setStyleSheet(
                open("src/ui/styles/dark_theme.qss").read()
            )
            self.btn_theme.setText("☀️")
            self.dark_mode = True
