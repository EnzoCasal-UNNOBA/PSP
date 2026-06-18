from src.services.activity_service import (
    create_activity,
    get_all_activities,
    get_activity_by_id,
    update_activity
)

resultado = update_activity(
    activity_id=1,
    fecha="2026-09-16",
    hora_inicio="10:00",
    hora_fin="12:30",
    interrupciones=10,
    descripcion="Actividad modificada",
    job_id=1
)

print()
print("Actualización:", resultado)

print()
print(get_activity_by_id(1))