from src.services.job_service import (
    create_job,
    get_all_jobs,
    create_task_type,
    get_all_task_types
)

nuevo_tipo = create_task_type(
    "Investigación"
)

print(f"Tipo creado con ID {nuevo_tipo}")

print()
print("TIPOS DE TAREA")
print()

for tipo in get_all_task_types():
    print(tipo)