from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget
)

from ui.pages.dashboard_page import DashboardPage
from ui.pages.activities_page import ActivitiesPage
from ui.pages.jobs_page import JobsPage
from ui.pages.categories_page import CategoriesPage
from ui.pages.reports_page import ReportsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PSP Manager")

        self.resize(1200, 700)

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QHBoxLayout()

        central_widget.setLayout(
            main_layout
        )

        # Menú lateral

        sidebar = QVBoxLayout()

        self.btn_dashboard = QPushButton(
            "Dashboard"
        )

        self.btn_activities = QPushButton(
            "Daily Log"
        )

        self.btn_jobs = QPushButton(
            "Jobs"
        )

        self.btn_categories = QPushButton(
            "Categorías"
        )

        self.btn_reports = QPushButton(
            "Reportes"
        )

        sidebar.addWidget(
            self.btn_dashboard
        )

        sidebar.addWidget(
            self.btn_activities
        )

        sidebar.addWidget(
            self.btn_jobs
        )

        sidebar.addWidget(
            self.btn_categories
        )

        sidebar.addWidget(
            self.btn_reports
        )

        sidebar.addStretch()

        # Stack de páginas

        self.stack = QStackedWidget()

        self.dashboard_page = DashboardPage()

        self.activities_page = ActivitiesPage()

        self.jobs_page = JobsPage()

        self.categories_page = CategoriesPage()

        self.reports_page = ReportsPage()

        self.stack.addWidget(
            self.dashboard_page
        )

        self.stack.addWidget(
            self.activities_page
        )

        self.stack.addWidget(
            self.jobs_page
        )

        self.stack.addWidget(
            self.categories_page
        )

        self.stack.addWidget(
            self.reports_page
        )

        main_layout.addLayout(
            sidebar,
            1
        )

        main_layout.addWidget(
            self.stack,
            4
        )

        self.connect_signals()
        
    def connect_signals(self):

        self.btn_dashboard.clicked.connect(
            lambda: self.stack.setCurrentIndex(0)
        )

        self.btn_activities.clicked.connect(
            lambda: self.stack.setCurrentIndex(1)
        )

        self.btn_jobs.clicked.connect(
            lambda: self.stack.setCurrentIndex(2)
        )

        self.btn_categories.clicked.connect(
            lambda: self.stack.setCurrentIndex(3)
        )

        self.btn_reports.clicked.connect(
            lambda: self.stack.setCurrentIndex(4)
        )