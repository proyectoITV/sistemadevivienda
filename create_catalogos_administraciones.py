import os
import django

# configure django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

create_sql = """
DROP TABLE IF EXISTS catalogos_administraciones;
CREATE TABLE catalogos_administraciones (
    idadministracion   SERIAL PRIMARY KEY,
    fechainicio        DATE                 NOT NULL,
    fechatermino       DATE                 NOT NULL,
    fecha_creacion     TIMESTAMP WITH TIME ZONE NOT NULL,
    id_empleado        INTEGER              NOT NULL,
    gobernador         VARCHAR(255)         NOT NULL
);
"""

inserts_sql = """
INSERT INTO catalogos_administraciones (fechainicio, fechatermino, fecha_creacion, id_empleado, gobernador) VALUES
('1993-02-05 00:00:00', '1999-02-04 23:59:59', '2024-03-05 00:00:00', 1308, 'Manuel Cavazos Lerma'),
('1999-02-05 00:00:00', '2004-12-31 23:59:59', '2024-03-05 00:00:00', 1308, 'Tomas Yarrington '),
('2005-01-01 00:00:00', '2010-12-31 23:59:59', '2024-03-05 00:00:00', 1308, 'Eugenio Hernández Flores'),
('2011-01-01 00:00:00', '2016-09-30 23:59:59', '2024-03-05 00:00:00', 1308, 'Egidio Torre Cantú'),
('2016-10-01 00:00:00', '2022-09-30 23:59:59', '2024-03-05 00:00:00', 1308, 'Francisco García Cabeza de Vaca'),
('2022-10-01 00:00:00', '2028-09-30 23:59:59', '2024-03-05 00:00:00', 1308, 'Americo Villarreal Anaya');
"""

with connection.cursor() as cur:
    cur.execute(create_sql)
    cur.execute(inserts_sql)

print("catalogos_administraciones table created and seeded")
