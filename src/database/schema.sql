CREATE TABLE IF NOT EXISTS tipos_tarea (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    activo INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    tipo_tarea_id INTEGER NOT NULL,

    fecha_creacion TEXT NOT NULL,

    estimado_tiempo INTEGER
        CHECK (estimado_tiempo >= 0),

    estimado_unidades REAL
        CHECK (estimado_unidades >= 0),

    real_unidades REAL
        CHECK (real_unidades >= 0),

    activo INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (tipo_tarea_id)
        REFERENCES tipos_tarea(id)
);

CREATE TABLE IF NOT EXISTS actividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT NOT NULL,

    hora_inicio TEXT NOT NULL,

    hora_fin TEXT NOT NULL,

    interrupciones INTEGER NOT NULL DEFAULT 0
        CHECK (interrupciones >= 0),

    descripcion TEXT,

    job_id INTEGER NOT NULL,

    FOREIGN KEY (job_id)
        REFERENCES jobs(id)
);

INSERT OR IGNORE INTO tipos_tarea(nombre)
VALUES
('Planificación'),
('Diseño'),
('Diseño detallado'),
('Codificación'),
('Compilación'),
('Testing'),
('Postmortem'),
('Comunicación'),
('Especificación'),
('Seguimiento');