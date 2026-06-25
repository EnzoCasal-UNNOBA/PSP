import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


app = QApplication(sys.argv)

# ---------------------------
# Cargar tema global
# ---------------------------

STYLE_PATH = (
    Path(__file__).parent
    / "ui"
    / "styles"
    / "light_theme.qss"
)

with open(STYLE_PATH, "r", encoding="utf-8") as file:
    app.setStyleSheet(file.read())

# ---------------------------
# Ventana principal
# ---------------------------

window = MainWindow()
window.show()

sys.exit(app.exec())