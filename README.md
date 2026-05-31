# PSP
Proyecto grupo C - Gestión de Proyectos 2026

# INSTALACION DE VENV Y POSIBLES ERRORES
1) Crear entorno virtual (venv):
    (windows): python -m venv .venv
    (Linux): python3 -m venv .venv

2) Activar venv:
    (Windows): .\.venv\Scripts\Activate.ps1
    Si aparece error de ejecucion de script ejecutar el siguiente comando (sin las " al comienzo y final) y luego el comando anterior: "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    (Linux): source .venv/bin/activate

3) Instalar dependencias:
    pip install -r requirements.txt

4) Actualizar dependencias
    pip install "nombre de la dependencia"
    pip freeze > requirements.txt (este comando actualiza el txt de dependencias asi no hay conflictos con las mismas)

5) Ejecutar proyecto
    python src/main.py