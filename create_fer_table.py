import os
import django

# configure django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

create_sql = """
DROP TABLE IF EXISTS fer_informacion;
CREATE TABLE fer_informacion (
    id                 SERIAL               PRIMARY KEY,
    nfer_id            INTEGER               NOT NULL,
    ejercicio          INTEGER               NOT NULL,
    numcertificado     INTEGER               NULL,
    contrato           VARCHAR(25)           NULL,
    nombre             VARCHAR(255)          NULL,
    curp               VARCHAR(18)           NULL,
    descripcion        TEXT                  NULL,
    cantidad           NUMERIC(15,2)         NULL,
    nfer_concepto_id   INTEGER               NULL REFERENCES fer_cat_subsidio(fer_idcon) ON DELETE RESTRICT,
    fechanacimiento    DATE                  NULL,
    domicilio          TEXT                  NULL,
    telefono           VARCHAR(20)           NULL,
    celular            VARCHAR(20)           NULL,
    autorizo           VARCHAR(255)          NULL,
    autorizo_fecha     DATE                  NULL,
    autorizo_hora      TIME WITHOUT TIME ZONE NULL,
    estado             INTEGER DEFAULT 0     NULL,
    parrafo_opcional   TEXT                  NULL,
    idempmodifica      INTEGER               NULL,
    fechaultimamod     DATE                  NULL,
    archivo_sustento   VARCHAR(100)          NULL,
    fecha_creacion     DATE                  NULL,
    fecha_modificacion_sistema DATE           NULL,
    id_municipio       INTEGER               NULL REFERENCES catalogos_municipios(id) ON DELETE RESTRICT,
    id_sexo            INTEGER               NULL REFERENCES catalogos_sexo(idsexo) ON DELETE RESTRICT,
    UNIQUE (nfer_id, ejercicio)
);
"""
with connection.cursor() as cur:
    cur.execute(create_sql)

print("fer_informacion table created or already existed")

# inspect columns
from django.db import connection
with connection.cursor() as cur:
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='fer_informacion';")
    cols = [row[0] for row in cur.fetchall()]
print("columns:", cols)
