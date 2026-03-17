from django.db import migrations, models
import django.db.models.deletion


def cargar_catalogos_vehiculos(apps, schema_editor):
    VehiculosMarcas = apps.get_model('anuncios', 'VehiculosMarcas')
    VehiculosColores = apps.get_model('anuncios', 'VehiculosColores')
    VehiculosEstatus = apps.get_model('anuncios', 'VehiculosEstatus')
    VehiculoPropietario = apps.get_model('anuncios', 'VehiculoPropietario')
    VehiculosTiposDeMantenimiento = apps.get_model('anuncios', 'VehiculosTiposDeMantenimiento')

    VehiculosMarcas.objects.bulk_create([
        VehiculosMarcas(clave_marca=1, marca='Chevrolet'),
        VehiculosMarcas(clave_marca=2, marca='Ford'),
        VehiculosMarcas(clave_marca=3, marca='Dodge'),
        VehiculosMarcas(clave_marca=4, marca='Nissan'),
        VehiculosMarcas(clave_marca=5, marca='Volkswagen'),
        VehiculosMarcas(clave_marca=6, marca='Suzuki'),
        VehiculosMarcas(clave_marca=7, marca='MG'),
    ], ignore_conflicts=True)

    VehiculosColores.objects.bulk_create([
        VehiculosColores(clave_color=1, color='Plata Metal'),
        VehiculosColores(clave_color=2, color='Blanco'),
        VehiculosColores(clave_color=3, color='Arena'),
        VehiculosColores(clave_color=4, color='Azul'),
        VehiculosColores(clave_color=5, color='Gris'),
        VehiculosColores(clave_color=6, color='Gris Metalico'),
        VehiculosColores(clave_color=7, color='Negro'),
        VehiculosColores(clave_color=8, color='Plata'),
        VehiculosColores(clave_color=9, color='Platino'),
        VehiculosColores(clave_color=10, color='Platino Metalico'),
        VehiculosColores(clave_color=11, color='Rojo'),
        VehiculosColores(clave_color=12, color='Verde'),
        VehiculosColores(clave_color=13, color='Azul Acerado'),
        VehiculosColores(clave_color=14, color='Blanco Olimpico'),
        VehiculosColores(clave_color=15, color='Blanco Oxford'),
        VehiculosColores(clave_color=16, color='Gris Arena'),
        VehiculosColores(clave_color=17, color='Gris Perla'),
        VehiculosColores(clave_color=18, color='Plata Metal 2'),
        VehiculosColores(clave_color=19, color='Rojo Quemado'),
    ], ignore_conflicts=True)

    VehiculosEstatus.objects.bulk_create([
        VehiculosEstatus(idestatus=0, estatus='Disponible'),
        VehiculosEstatus(idestatus=1, estatus='Inactivo'),
        VehiculosEstatus(idestatus=2, estatus='En Reparacion'),
        VehiculosEstatus(idestatus=3, estatus='En Comision'),
    ], ignore_conflicts=True)

    VehiculoPropietario.objects.bulk_create([
        VehiculoPropietario(idpropietario=1, propietario='ITAVU'),
        VehiculoPropietario(idpropietario=2, propietario='Arrendado'),
    ], ignore_conflicts=True)

    VehiculosTiposDeMantenimiento.objects.bulk_create([
        VehiculosTiposDeMantenimiento(clave_tipo_mant=0, tipo_mantenimiento='No Especificado'),
        VehiculosTiposDeMantenimiento(clave_tipo_mant=1, tipo_mantenimiento='Preventivo'),
        VehiculosTiposDeMantenimiento(clave_tipo_mant=2, tipo_mantenimiento='Correctivo'),
    ], ignore_conflicts=True)


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0038_transparenciago'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehiculosColores',
            fields=[
                ('clave_color', models.IntegerField(db_column='Clave_Color', primary_key=True, serialize=False)),
                ('color', models.CharField(blank=True, db_column='Color', max_length=255)),
            ],
            options={
                'verbose_name': 'Color de Vehiculo',
                'verbose_name_plural': 'Colores de Vehiculos',
                'db_table': 'vehiculos_colores',
                'ordering': ['clave_color'],
            },
        ),
        migrations.CreateModel(
            name='VehiculoPropietario',
            fields=[
                ('idpropietario', models.IntegerField(db_column='IdPropietario', primary_key=True, serialize=False)),
                ('propietario', models.CharField(blank=True, db_column='Propietario', max_length=255)),
            ],
            options={
                'verbose_name': 'Propietario de Vehiculo',
                'verbose_name_plural': 'Propietarios de Vehiculos',
                'db_table': 'vehiculo_propietario',
                'ordering': ['idpropietario'],
            },
        ),
        migrations.CreateModel(
            name='VehiculosEstatus',
            fields=[
                ('idestatus', models.IntegerField(db_column='IdEstatus', primary_key=True, serialize=False)),
                ('estatus', models.CharField(db_column='Estatus', max_length=255)),
            ],
            options={
                'verbose_name': 'Estatus de Vehiculo',
                'verbose_name_plural': 'Estatus de Vehiculos',
                'db_table': 'vehiculos_estatus',
                'ordering': ['idestatus'],
            },
        ),
        migrations.CreateModel(
            name='VehiculosMarcas',
            fields=[
                ('clave_marca', models.IntegerField(db_column='Clave_Marca', primary_key=True, serialize=False)),
                ('marca', models.CharField(blank=True, db_column='Marca', max_length=255)),
            ],
            options={
                'verbose_name': 'Marca de Vehiculo',
                'verbose_name_plural': 'Marcas de Vehiculos',
                'db_table': 'vehiculos_marcas',
                'ordering': ['clave_marca'],
            },
        ),
        migrations.CreateModel(
            name='VehiculosProveedores',
            fields=[
                ('clave_proveedor', models.IntegerField(db_column='clave_proveedor', primary_key=True, serialize=False)),
                ('nombre_proveedor', models.CharField(blank=True, db_column='Nombre_proveedor', max_length=255)),
            ],
            options={
                'verbose_name': 'Proveedor de Vehiculos',
                'verbose_name_plural': 'Proveedores de Vehiculos',
                'db_table': 'vehiculos_proveedores',
                'ordering': ['clave_proveedor'],
            },
        ),
        migrations.CreateModel(
            name='VehiculosTiposDeMantenimiento',
            fields=[
                ('clave_tipo_mant', models.IntegerField(db_column='clave_tipo_mant', primary_key=True, serialize=False)),
                ('tipo_mantenimiento', models.CharField(blank=True, db_column='Tipo_Mantenimiento', max_length=255)),
            ],
            options={
                'verbose_name': 'Tipo de Mantenimiento',
                'verbose_name_plural': 'Tipos de Mantenimiento',
                'db_table': 'vehiculos_tiposdemantenimiento',
                'ordering': ['clave_tipo_mant'],
            },
        ),
        migrations.CreateModel(
            name='Vehiculos',
            fields=[
                ('num_economico', models.CharField(db_column='Num_economico', max_length=255, primary_key=True, serialize=False)),
                ('tipo', models.CharField(blank=True, db_column='Tipo', max_length=255)),
                ('modelo', models.IntegerField(blank=True, db_column='Modelo', null=True)),
                ('placas', models.CharField(blank=True, db_column='Placas', max_length=255)),
                ('serie', models.CharField(blank=True, db_column='Serie', max_length=255)),
                ('revisado', models.CharField(blank=True, db_column='revisado', max_length=255)),
                ('comentario', models.TextField(db_column='Comentario')),
                ('cilindros', models.IntegerField(db_column='Cilindros')),
                ('clave_color', models.ForeignKey(blank=True, db_column='Clave_Color', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.vehiculoscolores')),
                ('clave_marca', models.ForeignKey(blank=True, db_column='Clave_marca', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.vehiculosmarcas')),
                ('idestatus', models.ForeignKey(db_column='IdEstatus', on_delete=django.db.models.deletion.RESTRICT, to='anuncios.vehiculosestatus')),
                ('idpropietario', models.ForeignKey(blank=True, db_column='IdPropietario', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.vehiculopropietario')),
            ],
            options={
                'verbose_name': 'Vehiculo',
                'verbose_name_plural': 'Vehiculos',
                'db_table': 'vehiculos',
                'ordering': ['num_economico'],
            },
        ),
        migrations.CreateModel(
            name='VehiculosBitacora',
            fields=[
                ('clave_servicio', models.AutoField(db_column='Clave_servicio', primary_key=True, serialize=False)),
                ('fecha_solicitud', models.DateTimeField(db_column='Fecha_solicitud')),
                ('fecha_ejecucion', models.DateTimeField(db_column='Fecha_ejecucion')),
                ('km_prog', models.IntegerField(db_column='Km_prog')),
                ('km_real', models.IntegerField(db_column='Km_real')),
                ('num_solicitud', models.IntegerField(db_column='num_solicitud')),
                ('num_factura', models.CharField(db_column='num_factura', max_length=255)),
                ('descripcion', models.CharField(db_column='Descripcion', max_length=1000)),
                ('costo_mano_obra', models.DecimalField(db_column='Costo_mano_obra', decimal_places=4, max_digits=19)),
                ('costo_refaccion', models.DecimalField(db_column='Costo_refaccion', decimal_places=4, max_digits=19)),
                ('importe_factura', models.DecimalField(db_column='Importe_factura', decimal_places=4, max_digits=19)),
                ('cancelada', models.BooleanField(db_column='Cancelada', default=False)),
                ('act_fecha', models.DateField(db_column='act_fecha')),
                ('act_hora', models.TimeField(db_column='act_hora')),
                ('act_user', models.CharField(db_column='act_user', max_length=50)),
                ('clave_proveedor', models.ForeignKey(db_column='clave_proveedor', on_delete=django.db.models.deletion.RESTRICT, to='anuncios.vehiculosproveedores')),
                ('clave_tipo_mant', models.ForeignKey(db_column='clave_tipo_mant', on_delete=django.db.models.deletion.RESTRICT, to='anuncios.vehiculostiposdemantenimiento')),
                ('num_economico', models.ForeignKey(db_column='Num_economico', on_delete=django.db.models.deletion.RESTRICT, to='anuncios.vehiculos')),
            ],
            options={
                'verbose_name': 'Bitacora de Vehiculo',
                'verbose_name_plural': 'Bitacora de Vehiculos',
                'db_table': 'vehiculos_bitacora',
                'ordering': ['-clave_servicio'],
            },
        ),
        migrations.RunPython(cargar_catalogos_vehiculos, migrations.RunPython.noop),
    ]
